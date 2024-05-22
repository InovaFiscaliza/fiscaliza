from .constants import SERVICOS

COMMON = {"status": "", "description": "", "start_date": "", "due_date": ""}

TECNICA = COMMON | {
    "custom_fields": {
        "data_de_inicio_efetivo": {
            "id": 627,
            "name": "Data de início efetivo",
            "value": "",
        },
        "classe_da_inspecao": {
            "id": 89,
            "name": "Classe da Inspeção",
            "value": {"valor": "", "texto": ""},
        },
        "tipo_de_inspecao": {
            "id": 2,
            "name": "Tipo de inspeção",
            "value": {"valor": "", "texto": ""},
        },
        "ano_de_execucao": {"id": 5, "name": "Ano de Execução", "value": ""},
        "tema": {
            "id": 14,
            "name": "Tema",
            "multiple": True,
            "value": [{"valor": "", "texto": ""}],
        },
        "subtema": {
            "id": 15,
            "name": "Subtema",
            "multiple": True,
            "value": [{"valor": "", "texto": ""}],
        },
        "coordenacao_responsavel": {
            "id": 178,
            "name": "Coordenação responsável",
            "value": "",
        },
        "no_sei_processo_fiscalizacao": {
            "id": 422,
            "name": "Nº SEI Processo Fiscalização",
            "replace_colon": True,
            "value": {"numero": ""},
        },
        "fiscal_responsavel": {"id": 25, "name": "Fiscal responsável", "value": ""},
        "fiscais": {"id": 26, "name": "Fiscais", "multiple": True, "value": [""]},
        "entidade_da_inspecao": {
            "id": 30,
            "name": "Entidade da Inspeção",
            "multiple": True,
            "value": [],
        },
        "ufmunicipio": {
            "id": 31,
            "name": "UF/Município",
            "multiple": True,
            "value": [{"valor": "", "texto": ""}],
        },
        "servicos_da_inspecao": {
            "id": 57,
            "name": "Serviços da Inspeção",
            "multiple": True,
            "map": SERVICOS,
            "value": [{"valor": "", "texto": ""}],
        },
        "horas_de_preparacao": {"id": 91, "name": "Horas de Preparação", "value": ""},
        "horas_de_deslocamento": {
            "id": 92,
            "name": "Horas de Deslocamento",
            "value": "",
        },
        "horas_de_execucao": {"id": 93, "name": "Horas de Execução", "value": ""},
        "horas_de_conclusao": {"id": 94, "name": "Horas de conclusão", "value": ""},
        "total_de_horas": {"id": 1789, "name": "Total de horas", "value": ""},
        "no_sav": {"id": 111, "name": "Nº SAV", "value": ""},
        "no_pcdp": {"id": 112, "name": "Nº PCDP", "value": ""},
        "altura_do_sistema_irradiante": {
            "id": 131,
            "name": "Altura do sistema irradiante",
            "value": "",
        },
        "uso_de_produto_homologado": {
            "id": 132,
            "name": "Uso de produto homologado?",
            "value": "",
        },
        "houve_obice": {"id": 136, "name": "Houve óbice?", "value": ""},
        "entidade_outorgada": {"id": 138, "name": "Entidade outorgada?", "value": ""},
        "esta_em_operacao": {"id": 139, "name": "Está em operação?", "value": ""},
        "situacao_constatada": {"id": 62, "name": "Situação constatada", "value": ""},
        "irregularidade": {
            "id": 73,
            "name": "Irregularidade",
            "multiple": True,
            "value": [],
        },
        "documento_instaurador_do_pado": {
            "id": 134,
            "name": "Documento instaurador do PADO",
            "value": "",
        },
        "potencia_medida": {"id": 81, "name": "Potência medida", "value": ""},
        "unidade_de_potencia": {"id": 82, "name": "Unidade de Potência", "value": ""},
        "frequencias": {"id": 180, "name": "Frequência(s)", "value": ""},
        "unidade_de_frequencia": {
            "id": 84,
            "name": "Unidade de Frequência",
            "value": "",
        },
        "procedimentos": {
            "id": 71,
            "name": "Procedimentos",
            "multiple": True,
            "value": [],
        },
        "utilizou_apoio_policial": {
            "id": 75,
            "name": "Utilizou apoio policial?",
            "value": "",
        },
        "houve_interferencia": {"id": 149, "name": "Houve interferência?", "value": ""},
        "situacao_de_risco_a_vida": {
            "id": 150,
            "name": "Situação de risco à vida?",
            "value": "",
        },
        "latitude_coordenadas": {
            "id": 170,
            "name": "Latitude (coordenadas)",
            "value": "",
        },
        "longitude_coordenadas": {
            "id": 171,
            "name": "Longitude (coordenadas)",
            "value": "",
        },
        "agrupamento": {"id": 213, "name": "Agrupamento", "value": ""},
        "app_fiscaliza": {"id": 463, "name": "App Fiscaliza", "value": ""},
        "precisa_reservar_instrumentos": {
            "id": 596,
            "name": "Precisa reservar instrumentos?",
            "value": "",
        },
        "utilizou_algum_instrumento": {
            "id": 598,
            "name": "Utilizou algum instrumento?",
            "value": "",
        },
        "utilizou_tecnicas_amostrais": {
            "id": 692,
            "name": "Utilizou técnicas amostrais?",
            "value": "",
        },
        "observacao_tecnica_amostral": {
            "id": 693,
            "name": "Observação (técnica amostral)",
            "value": "",
        },
        "coordenadas_geograficas": {
            "id": 717,
            "name": "Coordenadas Geográficas",
            "value": "",
        },
    },
}
