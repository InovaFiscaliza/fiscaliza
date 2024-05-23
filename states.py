FLOW = {
    "Rascunho": ["Aguardando Execução", "Cancelada"],
    "Aguardando Execução": ["Em Andamento", "Cancelada"],
    "Em Andamento": ["Aguardando Execução", "Relatando", "Relatada", "Cancelada"],
}
STATES = {
    "Técnica": {
        "Rascunho": ["status"],
        "Aguardando Execução": [
            "status",
            "description",
            "tipo_de_inspecao",
            "coordenacao_responsavel",
            "fiscal_responsavel",
            "fiscais",
        ],
        "Em Andamento": [
            "status",
            "description",
            "tipo_de_inspecao",
            "coordenacao_responsavel",
            "fiscal_responsavel",
            "fiscais",
            "precisa_reservar_instrumentos",
        ],
        "Relatando": [
            "status",
            "tipo_de_inspecao",
            "start_date",
            "due_date",
        ],
        "Relatada": [
            "status",
            "tipo_de_inspecao",
            "start_date",
            "due_date",
            "no_sei_processo_fiscalizacao",
            "entidade_com_cadastro_stel",
            "ufmunicipio",
            "horas_de_preparacao",
            "horas_de_execucao",
            "horas_de_deslocamento",
            "horas_de_conclusao",
            "houve_obice",
            "situacao_constatada",
            "endereco_da_inspecao",
            "qnt_produt_lacradosapreend",
            "utilizou_algum_instrumento",
            "utilizou_tecnicas_amostrais",
            "coordenadas_geograficas",
        ],
        "Opcional": [
            "entidade_da_inspecao",
            "servicos_da_inspecao",
            "no_sav",
            "no_pcdp",
            "documento_instaurador_do_pado",
            "procedimentos",
            "agrupamento",
            "area_do_pacp",
        ],
    }
}


[
    "servicos_da_inspecao",
    "notes",
    "agrupamento",
    "area_do_pacp",
]
