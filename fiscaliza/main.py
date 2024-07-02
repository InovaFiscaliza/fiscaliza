# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_main.ipynb.

# %% auto 0
__all__ = ["UTFCHARS", "Fiscaliza", "Issue"]

# %% ../nbs/00_main.ipynb 3
import copy
import json
import os
import re
from datetime import datetime, timedelta
from functools import cached_property
from pathlib import Path

import urllib3
from dotenv import load_dotenv
from fastcore.xtras import listify
from redminelib import Redmine
from requests.exceptions import ConnectionError, SSLError
from unidecode import unidecode

from .attrs import FIELDS
from .constants import FLOW, STATES, STATUS, URL_HM, URL_PD
from .datatypes import AtomicField

# %% ../nbs/00_main.ipynb 4
load_dotenv(override=True)

UTFCHARS = re.compile(r"[!\"#$%&'\(\)*+\,\-\.\/:;<=>\?@\[\\\]\^`_\{\|\}~]")


# %% ../nbs/00_main.ipynb 5
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


# %% ../nbs/00_main.ipynb 6
class Issue:
    def __init__(self, client: Redmine, issue_id: int | str):
        self.client = client
        self.id = issue_id
        self._issue = self.client.issue.get(
            issue_id,
            include=[
                "relations",
                "attachments",
                "journals",
                "allowed_statuses",
            ],
        )
        self._ascii2utf = {}

    @staticmethod
    def __format_json_string(field: str) -> str:
        """Recebe uma string formatada como json e retorna a mesma string formatada como json"""
        string = field.replace("'", '"').replace("=>", ": ")
        try:
            return json.loads(string)
        except (json.JSONDecodeError, TypeError):
            return string

    @staticmethod
    def extract_string(field: str) -> str | list:
        """Recebe uma string formatada como json e extrai os valores das chaves de acordo com o tipo de campo"""
        if isinstance(field, dict):
            if not (valor := field.get("valor")):
                valor = field.get("name", field)
            return str(valor)
        elif isinstance(field, str):
            json_obj = Issue.__format_json_string(field)
            if isinstance(json_obj, str):
                return json_obj
            return Issue.extract_string(json_obj)
        elif isinstance(field, list):
            fields = [Issue.extract_string(f) for f in field]
            if len(fields) == 1:
                return fields[0]
            return fields
        else:
            return str(field)

    @property
    def type(self) -> str:
        if tracker := self._attrs.get("tracker"):
            return self._utf2ascii(tracker.get("name", ""))

    def relations(self) -> dict:
        relations = {}
        for relation in self._attrs.get("relations", []):
            issue_id = relation.get("issue_id")
            if self._attrs["id"] == issue_id:
                issue_id = relation.get("issue_to_id")
            relations[issue_id] = Issue(self.client, issue_id)
        return relations

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

    def names2id(self) -> dict:
        return {
            member["user"]["name"]: member["user"]["id"]
            for member in self.project_members
            if "user" in member
        }

    def ids2names(self) -> dict:
        return {v: k for k, v in self.names2id().items()}

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

    def _extract_acao(self) -> dict:
        """
        Formats the relations of an issue as a dictionary.

        Returns:
            dict: A dictionary where the keys are the relation types, and the values are dictionaries containing the type, status, name, and description of the related issue.
        """
        for k, v in self.relations().items():
            if (type := getattr(v, "type", "")) == "acao_de_inspecao":
                return {
                    "type": type,
                    "status": Issue.extract_string(v._attrs.get("status")),
                    "name": v._attrs.get("subject"),
                    "description": v._attrs.get("description"),
                }
        return {}

    def _fiscais2ids(self, fiscais: list) -> list:
        if not isinstance(fiscais, list):
            fiscais = [fiscais]
        id_fiscais = []
        for fiscal in fiscais:
            if id_fiscal := self.names2id().get(fiscal):
                id_fiscais.append(id_fiscal)
        return id_fiscais

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

    def custom_fields(self) -> dict:
        custom_fields = {}
        for field in self._attrs.get("custom_fields", []):
            name = self._utf2ascii(field["name"])
            if name not in FIELDS:
                name = name.upper()
                self._ascii2utf[name] = field["name"]
            elif value := field.get("value"):
                if isinstance(value, str):
                    if "=>" in value:
                        name = name.upper()
                        self._ascii2utf[name] = field["name"]
            custom_fields[name] = field
        return custom_fields

    @cached_property
    def attrs(self) -> dict:
        """Retrieves the attributes of an issue as a dictionary."""
        special_fields = ["relations", "attachments", "custom_fields", "journals"]
        attrs = {}
        for k, v in self._attrs.items():
            if k in special_fields:
                continue
            elif k not in FIELDS:
                k = k.upper()
            attrs[k] = self.extract_string(v)

        attrs.update(
            {
                k: self.extract_string(v.get("value", ""))
                for k, v in self.custom_fields().items()
            }
        )
        attrs["ANEXOS"] = [
            file["content_url"] for file in self._attrs.get("attachments", [])
        ]
        attrs["ACAO"] = self._extract_acao()
        attrs["ATUALIZACAO"] = self.update_on()
        attrs["MEMBROS"] = list(self._issue_members().values())
        attrs["fiscal_responsavel"] = self.ids2names().get(
            attrs.get("fiscal_responsavel"), ""
        )
        attrs["fiscais"] = [
            self.ids2names().get(f, "") for f in listify(attrs.get("fiscais", []))
        ]
        return {k: attrs[k] for k in sorted(attrs)}

    @cached_property
    def editable_fields(self) -> dict:
        """Retrieves the editable fields of an issue as a dictionary."""
        editable_fields = {}
        for key, field in FIELDS.items():
            if key in self.attrs:
                setattr(field, "value", self.attrs[key])
                if key in ["fiscais", "fiscal_responsavel"]:
                    setattr(field, "options", self.attrs["MEMBROS"])
                editable_fields[key] = field
        return editable_fields

    def mandatory_fields(self) -> dict:
        return {
            k: v
            for k, v in self.editable_fields.items()
            if getattr(v, "mandatory", False)
        }

    def conditional_fields(self) -> dict:
        return {
            k: v
            for k, v in self.editable_fields.items()
            if getattr(v, "mapping", False)
        }

    def update_fields(self, dados: dict) -> dict:
        """
        Check if the data to be submitted to the Fiscaliza server is complete and valid.
        """
        if hasattr(self, "editable_fields"):
            del self.editable_fields

        for key, field in self.conditional_fields().items():
            if key in dados:
                if field.options:
                    for option in listify(dados[key]):
                        assert (
                            option in field.options
                        ), f"Opção inválida para o campo {key}: {option}"

                        # Since editable_fields commes from the .attrs, I need to clean fields based on conditional fields
                        # previously filled
                        for opt, values in field.mapping.items():
                            if opt != option:
                                self.editable_fields = {
                                    k: v
                                    for k, v in self.editable_fields.items()
                                    if k not in values
                                }
                        if new_fields := field.mapping.get(option):
                            self.editable_fields |= {k: FIELDS[k] for k in new_fields}

    def _get_id_only_fields(self, data: dict) -> dict:
        if status := data.get("status"):
            data["status"] = STATUS.get(status)
        if fiscais := data.get("fiscais"):
            if id_fiscais := self._fiscais2ids(fiscais):
                data["fiscais"] = id_fiscais
        if fiscal_responsavel := data.get("fiscal_responsavel"):
            if id_fiscal_responsavel := self.names2id().get(fiscal_responsavel):
                data["fiscal_responsavel"] = id_fiscal_responsavel
        return data

    def _check_coordinates(self, data: dict) -> dict:
        if (
            ("latitude_coordenadas" in data) and ("longitude_coordenadas" in data)
        ):  # Don't use numeric data that could be zero in clauses, that why the 'in' is here and not := dados.get(...)
            newkey = "coordenadas_geograficas"
            self.editable_fields[newkey] = FIELDS[newkey]
            self.editable_fields.pop("latitude_coordenadas")
            self.editable_fields.pop("longitude_coordenadas")
            data[newkey] = (
                data.pop("latitude_coordenadas"),
                data.pop("longitude_coordenadas"),
            )

        elif ("latitude_coordenadas" in data) != ("longitude_coordenadas" in data):
            raise ValueError(
                "Tanto 'latitude_coordenadas' quanto 'longitude_coordenadas' devem ser fornecidas juntas."
            )
        if ("latitude_da_estacao" in data) and ("longitude_da_estacao" in data):
            newkey = "coordenadas_estacao"
            self.editable_fields[newkey] = FIELDS[newkey]
            self.editable_fields.pop("latitude_da_estacao")
            self.editable_fields.pop("longitude_da_estacao")
            data[newkey] = (
                data.pop("latitude_da_estacao"),
                data.pop("longitude_da_estacao"),
            )

        elif ("latitude_da_estacao" in data) != ("longitude_da_estacao" in data):
            raise ValueError(
                "Tanto 'latitude_da_estacao' quanto 'longitude_da_estacao' devem ser fornecidas juntas."
            )
        return data

    def _validar_relatorio(self, dados):
        """Valida se o arquivo do relatório existe e está legível"""
        if dados.get("gerar_relatorio") == "1":
            self.editable_fields["gerar_relatorio"] = FIELDS["gerar_relatorio"]
            if (html_path := dados.get("html_path")) is None:
                raise ValueError(
                    "Foi solicitado a criação de um relatório no entanto o caminho para o arquivo html não foi fornecido"
                )
            html = Path(html_path)
            if not html.is_file():
                raise ValueError(f"Arquivo {html_path} não existe ou não é um arquivo")
            try:
                html_text = html.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                html_text = html.read_text(encoding="cp1252")
            dados["html"] = html_text
            self.editable_fields["html"] = FIELDS["html"]
            dados["relatorio_de_atividades"] = ""
            self.editable_fields["relatorio_de_atividades"] = FIELDS[
                "relatorio_de_atividades"
            ]
        else:
            self.editable_fields["gerar_relatorio"] = FIELDS["gerar_relatorio"]
            dados["gerar_relatorio"] = "0"
        if (relatorio := dados.get("relatorio_de_atividades")) is not None:
            dados["relatorio_de_atividades"] = relatorio
            self.editable_fields["relatorio_de_atividades"] = FIELDS[
                "relatorio_de_atividades"
            ]
        return dados

    def _check_uploads(self, dados: dict) -> list:
        uploads = []
        if (files := dados.get("uploads")) is not None:
            files = listify(files)
            for file in files:
                if not isinstance(file, dict):
                    raise ValueError(
                        "Os arquivos para upload devem ser fornecidos em um dicionário"
                    )
                if (path := file.get("path")) is not None:
                    if not Path(path).is_file():
                        raise ValueError(
                            f"Arquivo {path} não existe ou não é um arquivo"
                        )
                    uploads.append(file)
        return uploads

    def _check_submission(self, dados: dict):
        data = copy.deepcopy(dados)
        self.update_fields(data)
        data = self._validar_relatorio(data)
        data = {k: v for k, v in data.items() if k in self.editable_fields}
        data = self._get_id_only_fields(data)
        data = self._check_coordinates(data)
        return data

    def _parse_value_dict(self, dados: dict) -> dict:
        data = self._check_submission(dados)
        editable_fields = copy.deepcopy(self.editable_fields)
        data = {k: editable_fields[k](v) for k, v in data.items()}
        submitted_fields = {"custom_fields": []}
        if uploads := self._check_uploads(dados):
            submitted_fields["uploads"] = uploads
        for key, value in data.items():
            if isinstance(editable_fields[key], AtomicField):
                submitted_fields[editable_fields[key].name] = value
            else:
                submitted_fields["custom_fields"].append(value)
        return submitted_fields

    def refresh(self) -> None:
        """Refreshes the issue's attributes."""
        if hasattr(self, "editable_fields"):
            del self.editable_fields
        if hasattr(self, "_attrs"):
            del self._attrs
        if hasattr(self, "attrs"):
            del self.attrs
        self._issue = self.client.issue.get(
            self.id,
            include=[
                "relations",
                "attachments",
                "journals",
                "allowed_statuses",
            ],
        )

    def update(self, dados: dict):
        """Updates an issue with the given data."""
        self.refresh()
        status = self.editable_fields["status"].value
        for new_status in FLOW[status]:
            status_id = STATUS[new_status]
            if subset := STATES.get(new_status):
                subset = {k: v for k, v in dados.items() if k in subset}
                data = self._parse_value_dict(subset)
                self.client.issue.update(self.id, status_id=status_id, **data)
            else:
                data = self._parse_value_dict(dados)
                self.client.issue.update(self.id, status_id=status_id, **data)
            print(f"Atualizado para o status {new_status}")
            self.refresh()
