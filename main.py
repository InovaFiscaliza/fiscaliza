import os
import urllib3
from redminelib import Redmine

import typer
from requests.exceptions import SSLError, ConnectionError
from constants import URL_PD, URL_HM
from dotenv import load_dotenv

load_dotenv(override=True)


class Fiscaliza:
    def __init__(
        self, username: str, password: str, teste: bool = True, key: str = None
    ):
        self.username = username if key is None else os.environ["USERAPI"]
        self.password = password
        self.teste = teste
        self.key = key
        self.url = URL_HM if teste else URL_PD

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


class Issue:
    def __init__(self, fiscaliza: Fiscaliza, issue_id: int | str):
        self.fiscaliza = fiscaliza
        self.issue_id = issue_id
        self._issue = self.fiscaliza.issue.get(
            issue_id, include=["relations", "attachments"]
        )

    @staticmethod
    def _utf2ascii(s: str) -> str:
        """Receives a string and returns the same in ASCII format without spaces"""
        s = re.sub(UTFCHARS, "", s)
        return unidecode(s.replace(" ", "_"))

    @staticmethod
    def _format_json_string(field: str) -> str:
        """Recebe uma string formatada como json e retorna a mesma string formatada como json"""
        string = field.replace("'", '"').replace("=>", ": ")
        try:
            valor = json.loads(string)
            return valor
        except (json.JSONDecodeError, TypeError):
            return string
        return field

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
    def attrs(self):
        try:
            return dict(list(self.issue))
        except Exception:
            return {}
        
    @property
