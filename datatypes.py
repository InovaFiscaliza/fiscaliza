from dataclasses import dataclass
from itertools import product


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
        return value

    def validate_value(self, value: str | list) -> str | list:
        if self.multiple:
            values = []
            if not isinstance(value, list):
                raise ValueError("The value must be a list")
            for v in value:
                if not isinstance(v, str):
                    raise ValueError(f"The value must be a list of strings: {v}")
                values.append(self.format_value_string(v))
            return values
        else:
            if not isinstance(value, str):
                raise ValueError("The value must be a string")
            return self.format_value_string(value)

    def __call__(self, value: str | list) -> dict[str, str | list]:
        return {"id": self.id, "value": self.validate_value(value)}


@dataclass
class EncodedString(SimpleField):
    """This class always format the value string
    The json key is called 'numero'
    """

    def format_value_string(self, value: str) -> str:
        return "{" + '"numero"=>"{0}"'.format(value) + "}"


@dataclass
class FieldWithOptions(SimpleField):
    options: list[str]
    mapping: dict[str, list] = {}

    def __call__(self, value: str | list) -> dict[str, str | list]:
        if self.multiple:
            for v in value:
                if v not in self.options:
                    raise ValueError(f"The value {v} must be one of the valid options")
        else:
            if value not in self.options:
                raise ValueError(f"The value {value} must be one of the valid options")
        return {"id": self.id, "value": self.validate_value(value)}


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

    def __call__(self, latitude: str, longitude: str) -> dict[str, str]:
        if not isinstance(latitude, str) or not isinstance(longitude, str):
            raise ValueError("The latitude and longitude must be a string")
        return {"id": self.id, "value": self.format_value_string(latitude, longitude)}


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
        return {"id": self.id, "value": value}
