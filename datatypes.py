from typing import Dict, Optional
from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
    ValidationError,
)


class ValorTexto(BaseModel):
    value: str = Field(..., description="Valor do campo")

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, value: str) -> str:
        return "{" + '"valor":"{0}","texto":"{0}"'.format(value) + "}"


class SimpleField(BaseModel):
    id: int = Field(..., description="Id único do campo no Fiscaliza")
    name: str | None = Field(None, description="Nome do campo no Fiscaliza")
    value: str | list = Field(..., description="Valor recebido (não formatado)")
    mandatory: bool = Field(False, description="Campo obrigatório para a inspeção?")


class ComplementaryField(SimpleField):
    options: list[str] | None = Field(
        None, description="Lista de valores possíveis para o campo)"
    )
    multiple: bool = Field(False, description="Campo aceita mais de um valor?)")
    mapping: dict[str, list[str]] | None = Field(
        None, description="Mapeamento campos expostos à partir de valores preenchidos"
    )
