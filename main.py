import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from functools import cached_property

import typer
import urllib3
from dotenv import load_dotenv
from redminelib import Redmine
from requests.exceptions import ConnectionError, SSLError
from unidecode import unidecode

from constants import URL_HM, URL_PD, STATUS

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

    def get_issue(self, issue: str) -> dict:
        if issue_obj := self.issues.get(issue):
            return issue_obj
        issue_obj = Issue(self.client, issue)
        self.issues[issue] = issue_obj
        return issue_obj

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
    def __init__(self, client: Redmine, issue_id: int | str):
        self.client = client
        self.id = issue_id
        self._issue = self.client.issue.get(
            issue_id,
            include=[
                "relations",
                "attachments",
                # "children",
                "journals",
                # "changesets",
                # "watchers",
                "allowed_statuses",
            ],
        )
        self._ascii2utf = {}
        self._special_fields = set()
        self.editable_fields = {}
        self.init()

    def init(self):
        _ = self.attrs
        self.editable_fields["gerar_relatorio"] = "0"
        self.editable_fields["html"] = ""

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
            "description": "description",
            "status": "status_id",
            "start_date": "start_date",
            "due_date": "due_date",
        }

    @property
    def _composite_fields(self):
        return {
            "notes": "notes",
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

    @cached_property
    def _attrs(self) -> dict:
        _ = list(self._issue)
        self._issue.project.refresh()  # Prevent partial attrs return
        try:
            return dict(list(self._issue))
        except Exception as e:
            raise Exception(
                f"Não foi possível obter os atributos da issue {self.id}"
            ) from e

    @cached_property
    def custom_fields(self) -> dict:
        custom_fields = {}
        for field in self._attrs.get("custom_fields", []):
            name = self._utf2ascii(field["name"])
            if value := field.get("value"):
                if isinstance(value, str):
                    if "=>" in value:
                        # name = name.upper()
                        self._ascii2utf[name] = field["name"]
                        self._special_fields.add(name)
            custom_fields[name] = field
            if name not in self._special_fields:
                if (value := self.extract_string(value)) is None:
                    value = ""
                self.editable_fields[name] = value
        return custom_fields

    @cached_property
    def relations(self) -> dict:
        relations = {}
        for relation in self._attrs.get("relations", []):
            issue_id = relation.get("issue_id")
            if self._attrs["id"] == issue_id:
                issue_id = relation.get("issue_to_id")
            relations[issue_id] = Issue(self.client, issue_id)
        return relations

    @cached_property
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

    @cached_property
    def project_members(self) -> list:
        project_id = Issue.extract_string(self._attrs["project"]).lower()
        return [
            dict(member)
            for member in self.client.project_membership.filter(
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
                self.editable_fields[k] = self.extract_string(v)
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
        attrs["RELACOES"] = self._format_relations()
        attrs["ATUALIZACAO"] = self.update_on
        attrs["MEMBROS"] = list(self._issue_members().values())
        attrs["fiscal_responsavel"] = self.ids2names.get(
            attrs.get("fiscal_responsavel"), ""
        )
        attrs["fiscais"] = [self.ids2names.get(f, "") for f in attrs.get("fiscais", [])]
        return attrs

    def _utf2ascii(self, s: str) -> str:
        """Receives a string and returns the same in ASCII format without spaces"""
        decoded_string = unidecode(re.sub(UTFCHARS, "", s).replace(" ", "_")).lower()
        self._ascii2utf[decoded_string] = s
        return decoded_string

    def _issue_members(self, role: str = "Inspeção-Execução") -> dict:
        return {
            member["user"]["id"]: member["user"]["name"]
            for member in self.project_members
            if role in Issue.extract_string(member["roles"]) and "user" in member
        }

    def _format_relations(self) -> dict:
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

    def _fiscais2ids(self, fiscais: list) -> list:
        if not isinstance(fiscais, list):
            fiscais = [fiscais]
        id_fiscais = []
        for fiscal in fiscais:
            if id_fiscal := self.names2id.get(fiscal):
                id_fiscais.append(id_fiscal)
        return id_fiscais

    def _check_data(self, dados: dict) -> dict:
        data = dados.copy()
        if status := dados.get("status"):
            data["status"] = STATUS.get(status)
        if fiscais := dados.get("fiscais"):
            if id_fiscais := self._fiscais2ids(fiscais):
                data["fiscais"] = id_fiscais
        if fiscal_responsavel := dados.get("fiscal_responsavel"):
            if id_fiscal_responsavel := self.names2id.get(fiscal_responsavel):
                data["fiscal_responsavel"] = id_fiscal_responsavel
        return data

    # def refresh(self) -> None:
    #     """Refreshes the issue's attributes."""
    #     # for attr in self.__dict__:
    #     #     if isinstance(getattr(self.__class__, attr, None), cached_property):
    #     #         cached_attrs = getattr(self, attr)
    #     #         del cached_attrs  # Clear cache for each attribute
    #     self = Issue(self.client, self.id)
    #     self.init()

    def update(self, dados: dict) -> bool:
        """Updates an issue with the given data."""
        data = self._check_data(dados)
        submitted_fields = {"custom_fields": []}
        for k, v in self._atomic_fields.items():
            if k in data:
                submitted_fields[v] = data.pop(k)
        # Extract notes and upload
        for k, v in data.items():
            if value := self.custom_fields.get(k):
                value = {"id": value["id"], "value": v}
                submitted_fields["custom_fields"].append(value)
        print(submitted_fields)
        return self.client.issue.update(self.id, **submitted_fields)


def test_detalhar_issue(issue: str, teste: bool = True):
    from pprint import pprint

    fiscaliza = Fiscaliza(os.environ["USERNAME"], os.environ["PASSWORD"], teste)
    issue_obj = Issue(fiscaliza.client, issue)
    # pprint(issue_obj._attrs)
    # pprint(issue_obj.attrs)
    pprint(issue_obj.details)
    print(80 * "=")
    pprint(issue_obj.editable_fields)

    # pprint(Issue.extract_string(issue_obj.attrs["project"]).lower())

    json.dump(
        issue_obj.details,
        (Path.cwd() / f"{issue}.json").open("w"),
        indent=2,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    typer.run(test_detalhar_issue)
