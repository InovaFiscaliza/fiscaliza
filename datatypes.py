from dataclasses import dataclass
from itertools import product
from typing import Any

from fastcore.xtras import listify


class AtomicField(str):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.mandatory: bool = True

    def __call__(self, value):
        self.value = value
        return value

    def __repr__(self) -> str:
        string = ""
        if hasattr(self, "value"):
            string = f"(value: {self.value})"
        string += " | <mandatory>"
        return string


@dataclass
class SimpleField:
    id: int
    name: str
    mandatory: bool = False
    multiple: bool = False
    format_value: bool = False

    def format_value_string(self, value: str) -> str:
        if self.format_value:
            return "{" + '"valor":"{0}","texto":"{0}"'.format(value) + "}"
        try:
            value = str(value)
        except TypeError as e:
            raise ValueError(
                f"The value: {value} cannot be converted to a string"
            ) from e

        return value

    def validate_value(self, value: str | list) -> str | list:
        if self.multiple:
            return [self.format_value_string(v) for v in listify(value)]
        else:
            return self.format_value_string(value)

    def __call__(self, value: str | list) -> dict[str, str | list]:
        self.value = value
        return {"id": self.id, "value": self.validate_value(value)}

    def __repr__(self) -> str:
        string = ""
        if hasattr(self, "value"):
            string = f"(value: {self.value})"
        if self.mandatory:
            string += " | <mandatory>"
        if self.multiple:
            string += ", <multiple>"
        return string


@dataclass
class EncodedString(SimpleField):
    """This class always format the value string
    The json key is called 'numero'
    """

    def format_value_string(self, value: str) -> str:
        return "{" + '"numero"=>"{0}"'.format(value) + "}"

    def __repr__(self) -> str:
        string = ""
        if hasattr(self, "value"):
            string = f"({self.value})"
        if self.mandatory:
            string += " | <mandatory>"
        if self.multiple:
            string += ", <multiple>"
        return string


@dataclass
class FieldWithOptions(SimpleField):
    options: list[str] = None
    mapping: dict[str, list] = None

    def __call__(self, value: str | list) -> dict[str, str | list]:
        if self.multiple:
            value = [str(v) for v in listify(value)]
            for v in value:
                if (
                    self.options is not None and v not in self.options
                ):  # TODO: Corrigir gambiarra na classe Issue ( campo Fiscais ) e eliminar primeira condição
                    raise ValueError(f"The value {v} must be one of the valid options")
            if isinstance(self.options, dict):
                value = [self.options[v] for v in value]
        else:
            value = str(value)
            if self.options is not None and value not in self.options:
                raise ValueError(f"The value {value} must be one of the valid options")
            if isinstance(self.options, dict):
                value = self.options[value]
        self.value = value
        return {"id": self.id, "value": self.validate_value(value)}

    def __repr__(self) -> str:
        string = ""
        if hasattr(self, "value"):
            string = f"(value: {self.value})"
        if self.mandatory:
            string += " | <mandatory>"
        if self.multiple:
            string += ", <multiple>"
        if self.options:
            string += ", <options>"
        if self.mapping is not None:
            string += ", ⚠️conditional"
        return string


@dataclass
class Coordenadas:
    id: int
    name: str
    mandatory: bool = False

    def format_value_string(self, latitude: str, longitude: str) -> str:
        return (
            "{"
            + '"latitude"=>"{0}","longitude"=>"{1}"'.format(latitude, longitude)
            + "}"
        )

    def __call__(self, coords) -> dict[str, str]:
        latitude, longitude = coords[0], coords[1]
        self.value = (latitude, longitude)
        return {
            "id": self.id,
            "value": self.format_value_string(latitude, longitude),
        }

    def __repr__(self) -> str:
        string = ""
        if hasattr(self, "value"):
            string = f"(value: {self.value})"
        if self.mandatory:
            string += " | <mandatory>"
        return string


@dataclass
class GerarPlai:
    id: int
    name: str
    mandatory: bool = False
    TIPO_DE_PROCESSO = [
        "Gestão da Fiscalização: Lacração, Apreensão e Interrupção",
        "Gestão da Fiscalização: Processo de Guarda",
    ]
    COORD_FI = ["FI1", "FI2"]
    CODES = ["100000539", "100000618"]
    options = list(product(TIPO_DE_PROCESSO, COORD_FI))

    def validate_tipo_processo(self, value: str) -> str:
        options = dict(zip(self.TIPO_DE_PROCESSO, self.CODES))
        if value not in options:
            raise ValueError("tipo_processo is invalid")
        return options[value]

    def validate_coord_fi(self, value: str) -> str:
        if value not in self.COORD_FI:
            raise ValueError("coord_fi is invalid")
        return value

    def validate_values(self, tipo_processo: str, coord_fi: str) -> str:
        if tipo_processo == "" or coord_fi == "":
            return ""
        tipo_processo = self.validate_tipo_processo(tipo_processo)
        coord_fi = self.validate_coord_fi(coord_fi)
        return (
            "{"
            + '"criar_processo"=>"1","tipo_processo"=>"{0}","coord_fi"=>"{1}"'.format(
                tipo_processo, coord_fi
            )
            + "}"
        )

    def __call__(self, tipo_processo: str = "", coord_fi: str = "") -> dict[str, str]:
        value = self.validate_values(tipo_processo, coord_fi)
        self.value = {"id": self.id, "value": value}
        return self.value
