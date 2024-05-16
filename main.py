import json
import os
import re
from datetime import datetime, timedelta
from functools import cached_property
from typing import Iterator

import typer
import urllib3
from dotenv import load_dotenv
from redminelib import Redmine
from requests.exceptions import ConnectionError, SSLError
from unidecode import unidecode
from fastcore.xtras import dumps, Path

from constants import URL_HM, URL_PD

load_dotenv(override=True)

UTFCHARS = re.compile(r"[!\"#$%&'\(\)*+\,\-\.\/:;<=>\?@\[\\\]\^`_\{\|\}~]")


class Fiscaliza:
    def __init__(
        self, username: str, password: str, teste: bool = True, key: str = None
    ):
        self.username = username if key is None else os.environ["USERAPI"]
        self.password = password
        self.teste = teste
        self.key = key
        self.url = URL_HM if teste else URL_PD
        self.client = self.authenticate()
        self.issues = {}

    def authenticate(self):
        try:
            fiscaliza = Redmine(
                self.url,
                username=self.username,
                password=self.password,
                key=self.key,
                requests={"verify": True},
            )
            fiscaliza.auth()
        except SSLError:
            urllib3.disable_warnings()
            fiscaliza = Redmine(
                self.url,
                username=self.username,
                password=self.password,
                key=self.key,
                requests={"verify": False},
            )
            fiscaliza.auth()

        except ConnectionError as e:
            raise ConnectionError(
                "Não foi possível conectar ao servidor do Fiscaliza"
            ) from e
        return fiscaliza

    def issue_details(self, issue: str) -> dict:
        if self.issues.get(issue):
            return self.issues[issue].details
        issue_obj = Issue(self.client, issue)
        self.issues[issue] = issue_obj
        return issue_obj.details

    def save_cache(self, folder: Path):
        Path(folder).mkdir(exist_ok=True)
        for issue, issue_obj in self.issues.items():
            json.dump(
                issue_obj.details,
                (folder / f"{issue}.json").open("w"),
                ensure_ascii=False,
                indent=2,
            )


class Issue:
    def __init__(self, fiscaliza: Redmine, issue_id: int | str):
        self.fiscaliza = fiscaliza
        self.issue_id = issue_id
        self._issue = self.fiscaliza.issue.get(
            issue_id,
            include=[
                "relations",
                "attachments",
                "children",
                "journals",
                "changesets",
                "watchers",
                "allowed_statuses",
            ],
        )
        self._ascii2utf = {}
        self._special_fields = set()
        self.editable_fields = set()

    def _utf2ascii(self, s: str) -> str:
        """Receives a string and returns the same in ASCII format without spaces"""
        decoded_string = unidecode(re.sub(UTFCHARS, "", s).replace(" ", "_"))
        self._ascii2utf[decoded_string] = s
        return decoded_string

    @staticmethod
    def _format_json_string(field: str) -> str:
        """Recebe uma string formatada como json e retorna a mesma string formatada como json"""
        string = field.replace("'", '"').replace("=>", ": ")
        try:
            return json.loads(string)
        except (json.JSONDecodeError, TypeError):
            return string

    @staticmethod
    def extract_string(field: str) -> str | list:
        """Recebe uma string formatada como json e retorna somente o valor 'value' da string"""
        if isinstance(field, dict):
            if not (valor := field.get("valor")):
                valor = field.get("name", field)
            return valor
        if isinstance(field, str):
            json_obj = Issue._format_json_string(field)
            if isinstance(json_obj, str):
                return json_obj
            return Issue.extract_string(json_obj)
        if isinstance(field, list):
            return [Issue.extract_string(f) for f in field]
        return field

    @property
    def _atomic_fields(self):
        return {
            "project": "project_id",
            "subject": "subject",
            "tracker": "tracker_id",
            "description": "description",
            "status": "status_id",
            "priority": "priority_id",
            "assigned_to": "assigned_to_id",
            "parent": "parent_issue_id",
            "start_date": "start_date",
            "due_date": "due_date",
            "estimated_hours": "estimated_hours",
            "done_ratio": "done_ratio",
        }

    @property
    def _composite_fields(self):
        return {
            "notes": "notes",
            "private_notes": "private_notes",
            "custom_fields": "custom_fields",
            "uploads": "uploads",
        }

    @property
    def _fields(self):
        return self._atomic_fields | self._composite_fields

    @property
    def type(self) -> str:
        if tracker := self._attrs.get("tracker"):
            return self._utf2ascii(tracker.get("name", ""))

    @property
    def _attrs(self) -> dict:
        try:
            return dict(list(self._issue))
        except Exception as e:
            raise Exception(
                f"Não foi possível obter os atributos da issue {self.issue_id}"
            ) from e

    @property
    def custom_fields(self) -> dict:
        custom_fields = {}
        for field in self._attrs.get("custom_fields", []):
            name = self._utf2ascii(field["name"])
            if value := field.get("value"):
                if isinstance(value, str):
                    if "=>" in value:
                        name = name.upper()
                        self._ascii2utf[name] = field["name"]
                        self._special_fields.add(name)
            custom_fields[name] = field
        return custom_fields

    @property
    def relations(self) -> dict:
        relations = {}
        for relation in self._attrs.get("relations", []):
            issue_id = relation.get("issue_id")
            if self._attrs["id"] == issue_id:
                issue_id = relation.get("issue_to_id")
            relations[issue_id] = Issue(self.fiscaliza, issue_id)
        return relations

    @cached_property
    def project_members(self) -> list:
        project_id = Issue.extract_string(self._attrs["project"]).lower()
        return [
            dict(member)
            for member in self.fiscaliza.project_membership.filter(
                project_id=project_id, limit=None
            )
        ]

    @cached_property
    def names2id(self) -> dict:
        return {
            member["user"]["name"]: member["user"]["id"]
            for member in self.project_members
            if "user" in member
        }

    @cached_property
    def ids2names(self) -> dict:
        return {v: k for k, v in self.names2id.items()}

    def _utf2ascii(self, s: str) -> str:
        """Receives a string and returns the same in ASCII format without spaces"""
        decoded_string = unidecode(re.sub(UTFCHARS, "", s).replace(" ", "_").lower())
        self._ascii2utf[decoded_string] = s
        return decoded_string

    def issue_members(self, role: str = "Inspeção-Execução") -> dict:
        return {
            member["user"]["id"]: member["user"]["name"]
            for member in self.project_members
            if role in Issue.extract_string(member["roles"]) and "user" in member
        }

    def update_on(self) -> str:
        if journal := self._attrs["journals"]:
            journal = journal[-1]
            key = "user"
        else:
            journal = self._attrs
            key = "author"

        user = journal[key]["name"]
        date = datetime.strptime(
            journal["created_on"], "%Y-%m-%dT%H:%M:%SZ"
        ) - timedelta(hours=3)
        return f"Atualizado por {user} em {datetime.strftime(date, '%d/%m/%Y')} às {date.time()}"

    def format_relations(self) -> dict:
        """
        Formats the relations of an issue as a dictionary.

        Returns:
            dict: A dictionary where the keys are the relation types, and the values are dictionaries containing the type, status, name, and description of the related issue.
        """
        relations = {}
        for k, v in self.relations.items():
            relations[k] = {
                "type": getattr(v, "type"),
                "status": Issue.extract_string(v._attrs.get("status")),
                "name": v._attrs.get("subject"),
                "description": v._attrs.get("description"),
            }
        return relations

    @cached_property
    def attrs(self) -> dict:
        """Retrieves the attributes of an issue as a dictionary."""
        special_fields = ["relations", "attachments", "custom_fields", "journals"]
        attrs = {}
        for k, v in self._attrs.items():
            if k in special_fields:
                continue
            elif k not in self._fields:
                k = k.upper()
            else:
                self.editable_fields.add(k)
            attrs[k] = v
        attrs["custom_fields"] = self.custom_fields
        return attrs

    @cached_property
    def details(self) -> dict:
        """Retrieves the details of an issue as a dictionary.

        Returns:
            dict: A dictionary containing the details of the issue, including its attachments, custom fields, journals, and other relevant information.
        """
        attrs = self.attrs.copy()
        attrs.update(
            {k: v.get("value", "") for k, v in attrs.pop("custom_fields").items()}
        )
        attrs = {k: self.extract_string(v) for k, v in attrs.items()}
        attrs["ANEXOS"] = [
            file["content_url"] for file in self._attrs.get("attachments", [])
        ]
        attrs["RELACOES"] = self.format_relations()
        attrs["ATUALIZACAO"] = self.update_on()
        attrs["MEMBROS"] = list(self.issue_members().values())
        attrs["fiscal_responsavel"] = self.ids2names.get(
            attrs.get("fiscal_responsavel"), ""
        )
        attrs["fiscais"] = [self.ids2names.get(f, "") for f in attrs.get("fiscais", [])]
        return attrs


def test_detalhar_issue(issue: str, teste: bool = True):
    from pprint import pprint

    fiscaliza = Fiscaliza(os.environ["USERNAME"], os.environ["PASSWORD"], teste)
    issue_obj = Issue(fiscaliza.client, issue)
    # pprint(issue_obj._attrs)
    pprint(issue_obj.attrs)
    pprint(issue_obj.details)
    pprint(issue_obj._fields)

    # pprint(Issue.extract_string(issue_obj.attrs["project"]).lower())

    json.dump(
        issue_obj.details,
        (Path.cwd() / f"{issue}.json").open("w"),
        indent=2,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    typer.run(test_detalhar_issue)
