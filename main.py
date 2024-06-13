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
from fastcore.xtras import listify

from constants import URL_HM, URL_PD, STATUS
from attrs import FIELDS
from datatypes import AtomicField


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
        """Recebe uma string formatada como json e retorna somente o valor 'value' da string"""
        if isinstance(field, dict):
            if not (valor := field.get("valor")):
                valor = field.get("name", field)
            return valor
        if isinstance(field, str):
            json_obj = Issue.__format_json_string(field)
            if isinstance(json_obj, str):
                return json_obj
            return Issue.extract_string(json_obj)
        if isinstance(field, list):
            return [Issue.extract_string(f) for f in field]
        return field

    @property
    def type(self) -> str:
        if tracker := self._attrs.get("tracker"):
            return self._utf2ascii(tracker.get("name", ""))

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
                for k, v in self.custom_fields.items()
            }
        )
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
        return {k: attrs[k] for k in sorted(attrs)}

    @cached_property
    def info_fields(self) -> dict:
        return {k: v for k, v in self.attrs.items() if k.isupper()}

    @cached_property
    def editable_fields(self) -> dict:
        """Retrieves the editable fields of an issue as a dictionary."""
        editable_fields = {}
        for key, field in FIELDS.items():
            if key in self.attrs:
                setattr(field, "value", self.attrs[key])
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

                        if new_fields := field.mapping.get(option):
                            # Since editable_fields commes from the .attrs, I need to clean fields based on conditional fields
                            # previously filled
                            for opt, values in field.mapping.items():
                                if opt != option:
                                    self.editable_fields = {
                                        k: v
                                        for k, v in self.editable_fields.items()
                                        if k not in values
                                    }
                            self.editable_fields |= {k: FIELDS[k] for k in new_fields}

    def _get_id_only_fields(self, data: dict) -> dict:
        if status := data.get("status"):
            data["status"] = STATUS.get(status)
        if fiscais := data.get("fiscais"):
            if id_fiscais := self._fiscais2ids(fiscais):
                data["fiscais"] = id_fiscais
        if fiscal_responsavel := data.get("fiscal_responsavel"):
            if id_fiscal_responsavel := self.names2id.get(fiscal_responsavel):
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

    def _check_submission(self, dados: dict):
        self.update_fields(dados)
        data = {k: v for k, v in dados.items() if k in self.editable_fields}
        data = self._get_id_only_fields(data)
        data = self._check_coordinates(data)
        for key in self.mandatory_fields():
            assert key in data, f"Dado obrigatório: {key}"
        return data

    def _parse_value_dict(self, dados: dict) -> dict:
        return {
            k: self.editable_fields[k](v)
            for k, v in self._check_submission(dados).items()
        }

    def refresh(self) -> None:
        """Refreshes the issue's attributes."""
        for attr in self.__dict__:
            if isinstance(getattr(self.__class__, attr, None), cached_property):
                cached = getattr(self, attr)  # Clear cache for each attribute
                del cached
        self.init()

    def update(self, dados: dict) -> bool:
        """Updates an issue with the given data."""
        data = self._parse_value_dict(dados)
        submitted_fields = {"custom_fields": []}
        # Extract notes and upload
        for key, value in data.items():
            if isinstance(self.editable_fields[key], AtomicField):
                submitted_fields[self.editable_fields[key].name] = value
            else:
                submitted_fields["custom_fields"].append(value)
        return self.client.issue.update(self.id, **submitted_fields)


def test_detalhar_issue(issue: str, teste: bool = True):
    fiscaliza = Fiscaliza(os.environ["USERNAME"], os.environ["PASSWORD"], teste)
    issue_obj = Issue(fiscaliza.client, issue)
    # pprint(issue_obj.attrs)
    dados = {
        "agrupamento": "10",
        "altura_do_sistema_irradiante": "10",
        "ano_de_execucao": 2025,
        "app_fiscaliza": "1",
        "classe_da_inspecao": "Tributária",
        "coordenacao_responsavel": "FI2",
        "coordenadas_geograficas": "",
        "data_de_inicio_efetivo": "01/05/2024",
        "description": "[PMEC 2024 Etapa 2] Monitorar canais e faixas de frequências "
        "relacionados às aplicações críticas (como, por exemplo, "
        "radionavegação e radiocomunicação aeronáutica e canais de "
        "emergência) na forma a ser estabelecida no Plano de Ação de "
        "Fiscalização.\r\n",
        "documento_instaurador_do_pado": "",
        "due_date": "30/06/2024",
        "entidade_da_inspecao": [],
        "entidade_outorgada": "",
        "esta_em_operacao": "",
        "fiscais": ["Ronaldo da Silva Alves Batista"],
        "fiscal_responsavel": "Ronaldo da Silva Alves Batista",
        "frequencias": "",
        "gerar_relatorio": "0",
        "horas_de_conclusao": "",
        "horas_de_deslocamento": "",
        "horas_de_execucao": "",
        "horas_de_preparacao": "",
        "houve_interferencia": "",
        "houve_obice": "",
        "html": "",
        "irregularidade": [],
        "latitude_coordenadas": "",
        "longitude_coordenadas": "",
        "no_pcdp": "",
        "no_sav": "",
        "observacao_tecnica_amostral": "",
        "potencia_medida": "",
        "precisa_reservar_instrumentos": "",
        "procedimentos": [],
        "servicos_da_inspecao": [],
        "situacao_constatada": "",
        "situacao_de_risco_a_vida": "",
        "start_date": "2024-03-01",
        "status": "Rascunho",
        "subtema": ["Radiomonitoração Terrestre"],
        "tema": ["Uso do Espectro"],
        "tipo_de_inspecao": '{"valor":"Outorga - Aspectos Técnicos","texto":"Outorga - Aspectos Técnicos"}',
        "total_de_horas": 0.0,
        "ufmunicipio": ['{"valor":"SP/Jundiaí","texto":"SP/Jundiaí"}'],
        "unidade_de_frequencia": "",
        "unidade_de_potencia": "",
        "uso_de_produto_homologado": "",
        "utilizou_algum_instrumento": "",
        "utilizou_apoio_policial": "",
        "utilizou_tecnicas_amostrais": "",
    }
    print(
        issue_obj.client.issue.update(
            issue,
            custom_fields=[
                {
                    "id": 426,
                    "value": '{"criar_processo"=>"1","tipo_processo"=>"100000539","coord_fi"=>"FI4"}',
                }
            ],
        )
    )


if __name__ == "__main__":
    typer.run(test_detalhar_issue)
