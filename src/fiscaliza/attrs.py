# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_attrs.ipynb.

# %% auto 0
__all__ = ["SPECIAL_FIELDS", "FIELDS"]

# %% ../nbs/03_attrs.ipynb 2
from fiscaliza.datatypes import (
    AtomicField,
    SimpleField,
    EncodedString,
    FieldWithOptions,
    Coordenadas,
    GerarPlai,
)
from fiscaliza.constants import MUNICIPIOS, SERVICOS


# %% ../nbs/03_attrs.ipynb 3
SPECIAL_FIELDS = {
    "coordenadas_estacao": Coordenadas(718, "Coordenadas Estação"),
    "coordenadas_geograficas": Coordenadas(717, "Coordenadas Geográficas", True),
    "gerar_plai": GerarPlai(426, "Gerar PLAI?"),
    "outras_fontes_interferentes": EncodedString(  # NotImplemented
        2076, "Outras fontes interferentes:", True
    ),
}

FIELDS = {
    "status": AtomicField("Situação", "status_id", mandatory=False),
    "description": AtomicField("Descrição", "description"),
    "start_date": AtomicField("Data de início", "start_date"),
    "due_date": AtomicField("Data limite", "due_date"),
    "acao_de_risco_a_vida_criada": FieldWithOptions(
        154,
        "Ação de risco à vida criada?",
        options=["", "Não", "Sim"],
        mapping={"Sim": ["acao_de_risco_a_vida"]},
    ),
    "acao_de_risco_a_vida": FieldWithOptions(
        155, "Ação de risco à vida", multiple=True, format_value=True, options=[]
    ),
    "agrupamento": SimpleField(213, "Agrupamento:"),
    "altura_do_sistema_irradiante": SimpleField(131, "Altura do sistema irradiante:"),
    "area_do_pacp": FieldWithOptions(
        416,
        "Área do PACP:",
        options=[
            "",
            "1-Comércio",
            "2-ISP",
            "3-E-commerce",
            "4-Aduana",
            "5-Feiras e Eventos",
            "6-Supervisão de Mercados",
        ],
    ),
    "campo_eletrico__pico_vm": SimpleField(195, "Campo elétrico pico (V/m):", True),
    "campo_eletrico_rms_vm": SimpleField(194, "Campo elétrico RMS (V/m):", True),
    "cnpjcpf_da_entidade": SimpleField(141, "CNPJ/CPF da Entidade:"),
    "coordenacao_responsavel": FieldWithOptions(
        178, "Coordenação responsável:", options=["", "FI", "FI1", "FI2", "FI3"]
    ),
    "coord_fi_plai": FieldWithOptions(
        426, "Coordenação PLAI:", options=["", "FI", "FI1", "FI2", "FI3"]
    ),
    "copiar_instrumento_da_reserva": FieldWithOptions(
        629, "Copiar instrumento da reserva?", options=["", "0", "1"]
    ),
    "documento_instaurador_do_pado": SimpleField(134, "Documento instaurador do PADO:"),
    "endereco_da_inspecao": SimpleField(142, "Endereço da Inspeção:", True),
    "entidade_com_cadastro_stel": FieldWithOptions(
        189,
        "Entidade com cadastro STEL?",
        mandatory=True,
        options=["", "Não", "Sim"],
        mapping={
            "Sim": ["entidade_da_inspecao"],
            "Não": ["nome_da_entidade", "cnpjcpf_da_entidade"],
        },
    ),
    "entidade_da_inspecao": FieldWithOptions(
        30, "Entidade da Inspeção:", multiple=True, format_value=True, options=[]
    ),
    "entidade_outorgada": FieldWithOptions(
        138,
        "Entidade Outorgada?",
        mandatory=True,
        options=["", "0", "1"],
        mapping={"1": ["numero_da_estacao"]},
    ),
    "esta_em_operacao": FieldWithOptions(
        139, "Está em operação?", mandatory=True, options=["", "0", "1"]
    ),
    "fiscais": FieldWithOptions(26, "Fiscais:", mandatory=True, multiple=True),
    "fiscal_responsavel": FieldWithOptions(25, "Fiscal responsável:", mandatory=True),
    "foi_constatada_interferencia": FieldWithOptions(
        1967,
        "Foi constatada interferência?",
        mandatory=True,
        options=["", "0", "1"],
        mapping={
            "0": ["justificativa_da_improcedencia"],
            "1": [
                "interferencia_sanada",
                "local_interf_confere_indicado",
                "tipo_de_fonte_interferente",
                "fonte_e_modelo",
                "frequencia_mhz",
                "potencia_de_operacao_w",
                "homologada",
                "ha_outras_fontes_interfer",
            ],
        },
    ),
    "fonte_e_modelo": SimpleField(
        2069,
        "Fonte e modelo:",
    ),
    "frequencia_mhz": SimpleField(
        2071,
        "Frequência (MHz):",
    ),
    "frequencia_inicial": SimpleField(156, "Frequência inicial:", True, _dtype="float"),
    "frequencia_final": SimpleField(158, "Frequência final:", True, _dtype="float"),
    "frequencias": SimpleField(180, "Frequência(s):"),
    "gerar_plai": FieldWithOptions(
        426,
        "Gerar PLAI?",
        options=["", "0", "1"],
        mapping={"1": ["tipo_do_processo_plai", "coord_fi_plai"]},
    ),
    "gerar_relatorio": FieldWithOptions(
        541,
        "Gerar Relatório",
        options=["", "0", "1"],
        mapping={"1": ["html"]},
    ),
    "ha_outras_fontes_interfer": FieldWithOptions(
        2075,
        "Há outras fontes interferentes?",
        mandatory=True,
        options=["", "Não", "Sim"],
    ),
    "homologada": FieldWithOptions(
        2074,
        "Homologada?",
        mandatory=True,
        options=["", "Não", "Sim", "Indeterminado"],
    ),
    "horas_de_conclusao": SimpleField(94, "Horas de conclusão", True, _dtype="float"),
    "horas_de_deslocamento": SimpleField(
        92, "Horas de deslocamento", True, _dtype="float"
    ),
    "horas_de_execucao": SimpleField(93, "Horas de Execução", True, _dtype="float"),
    "horas_de_preparacao": SimpleField(91, "Horas de Preparação", True, _dtype="float"),
    "houve_interferencia": FieldWithOptions(
        149,
        "Houve interferência?",
        mandatory=True,
        options=[
            "",
            "Não",
            "Sim",
        ],
        mapping={"Sim": ["identificada_a_origem"]},
    ),
    "houve_obice": FieldWithOptions(
        136, "Houve óbice?", mandatory=True, options=["", "0", "1"]
    ),
    "html": SimpleField(543, "Html", True),
    "identificada_a_origem": FieldWithOptions(
        162,
        "Identificada a origem?",
        mandatory=True,
        options=["", "0", "1"],
        mapping={"1": ["sanada_ou_mitigada"]},
    ),
    "identificacao_da_nao_outorgada": SimpleField(
        250, "Identificação da Não Outorgada:"
    ),
    "instrumentos_utilizados": FieldWithOptions(
        599, "Instrumentos Utilizados", True, True, options=[]
    ),
    "interferencia_sanada": FieldWithOptions(
        1969,
        "Interferência sanada?",
        mandatory=True,
        options=[
            "",
            "Sim, confirmado pelo denunciante",
            "Sim, sem confirmação pelo denunciante",
            "Não",
        ],
        mapping={
            "Sim, sem confirmação pelo denunciante": ["justificativa_nao_confirmacao"],
            "Não": ["justificativa_nao_resolucao"],
        },
    ),
    "irregularidade": FieldWithOptions(
        73,
        "Irregularidade:",
        multiple=True,
        options=[],  # Preechido dinamicamente dentro da classe Issue
        format_value=True,
    ),
    "justificativa_da_improcedencia": FieldWithOptions(
        1968,
        "Justificativa da Improcedência:",
        options=[
            "",
            "Reclamante informou que interferência cessou",
            "Dados obtidos indicam que interferência não procede",
            "Não foi constatada portadora interferente em campo",
        ],
    ),
    "justificativa_nao_confirmacao": SimpleField(
        1970,
        "Justificativa não confirmação:",
        mandatory=True,
    ),
    "justificativa_nao_resolucao": SimpleField(
        1971, "Justificativa não resolução:", mandatory=True
    ),
    # "lai_vinculadas": SimpleField(481, "LAI vinculadas"),
    "latitude_coordenadas": SimpleField(170, "Latitude (º):", True),
    "latitude_da_estacao": SimpleField(191, "Latitude da estação (º):", True),
    "local_interf_confere_indicado": FieldWithOptions(
        1972,
        "Local interferência confere indicado?",
        mandatory=True,
        options=["", "Sim", "Não", "Parcialmente", "Não se aplica"],
    ),
    "longitude_coordenadas": SimpleField(171, "Longitude (º):", True),
    "longitude_da_estacao": SimpleField(192, "Longitude da estação (º):", True),
    "motivo_de_lai": FieldWithOptions(
        164,
        "Motivo de LAI:",
        mandatory=True,
        multiple=True,
        options=[
            "Risco à vida",
            "Clandestinidade",
            "Interferência prejudicial",
            "Uso de produto não certificado",
            "Garantir a segurança (exposição a campos eletromagnéticos)",
            "Necessidade de assegurar o planejamento, o gerenciamento e a coordenação do uso de espectro de radiofrequências (justificar)",
        ],
    ),
    "numero_da_estacao": SimpleField(137, "Número da estação:", True),
    "numero_do_pai": SimpleField(211, "Nº SEI PAI:"),
    "no_de_homologacao": SimpleField(161, "Nº de Homologação:"),
    "no_do_lacre": SimpleField(165, "Nº do lacre:", True),
    "no_pcdp": SimpleField(112, "Nº PCDP:"),
    "no_sav": SimpleField(111, "Nº SAV:"),
    "no_sei_do_aviso_lai": EncodedString(427, "Nº SEI Referendo (Aviso LAI):", True),
    "no_sei_do_oficio_ao_mctic": EncodedString(428, "Nº SEI do Ofício ao MCTIC:"),
    "no_sei_do_plaiguarda": EncodedString(426, "Nº SEI PLAI:"),
    "no_sei_processo_fiscalizacao": EncodedString(422, "Nº SEI PFIS:"),
    "no_sei_relatorio_de_atividades": SimpleField(544, "Nº SEI Relatório:"),
    "nome_da_entidade": SimpleField(140, "Nome da Entidade:", True),
    "observacao_tecnica_amostral": SimpleField(
        693, "Observação (técnica amostral):", True
    ),
    "observacoes": SimpleField(1973, "Observações:"),
    "pai_instaurado_pela_anatel": FieldWithOptions(
        160,
        "PAI instaurado pela Anatel?",
        True,
        options=["", "Não", "Sim"],
        mapping={"Sim": ["numero_do_pai"]},
    ),
    "potencia_de_operacao_w": SimpleField(2072, "Potência de Operação (W):", True),
    "potencia_medida": SimpleField(81, "Potência:"),
    "precisa_reservar_instrumentos": FieldWithOptions(
        596,
        "Precisa reservar instrumentos?",
        mandatory=True,
        options=["", "0", "1"],
        mapping={"1": ["reserva_de_instrumentos"]},
    ),
    "procedimentos": FieldWithOptions(
        71,
        "Procedimentos:",
        mandatory=True,
        multiple=True,
        options=[
            "Nenhum",
            "Lacração",
            "Apreensão",
            "Interrupção",
            "Não Cadastrado",
            "Notificado",
            "A Notificar",
            "Liberação/Desinterrupção",
            "Orientação ao Usuário",
            "Comunicado",
            "Deslacrado",
            "Vistoriado",
            "Emissão Termo Violação de Lacre",
            "Apoio a busca e apreensão",
            "Investigação/Pesquisa",
            "Não Lacrado - Impedimento",
            "Não Lacrado - Amparo Judicial",
            "Não Lacrado - Responsável Ausente",
            "Não Lacrado - Local Fechado",
            "Constatação Violação Lacre/Relacrado",
            "Constatação Violação Lacre/Impedimento",
            "Notícia Crime",
            "Monitorado alterado",
            "Constatação Encerramento - Informe",
            "Levantamento de Dados",
            "Análise/coleta de Dados",
            "Monitorado",
            "Não Lacrado - Desativado",
            "Devolução de Produto(s)",
            "Outros",
        ],
        mapping={
            "Lacração": [
                "no_do_lacre",
                "motivo_de_lai",
                "no_sei_do_aviso_lai",
                # "lai_vinculadas",
                "no_sei_do_plaiguarda",
                "gerar_plai",
            ],
            "Apreensão": [
                "motivo_de_lai",
                "no_sei_do_aviso_lai",
                # "lai_vinculadas",
                "no_sei_do_plaiguarda",
                "gerar_plai",
            ],
            "Interrupção": [
                "motivo_de_lai",
                "no_sei_do_aviso_lai",
                # "lai_vinculadas",
                "no_sei_do_plaiguarda",
                "gerar_plai",
            ],
        },
    ),
    "qnt_produt_lacradosapreend": SimpleField(
        143, "Qtd. produtos lacrados ou apreendidos:", True, _dtype="int"
    ),
    "qtd_de_emissoes": SimpleField(69, "Qtd. Emissões:", _dtype="int"),
    "qtd_identificadas": SimpleField(731, "Qtd. Identificadas:", _dtype="int"),
    "qtd_licenciadas": SimpleField(730, "Qtd. Licenciadas:", _dtype="int"),
    "relatorio_de_atividades": EncodedString(544, "Nº SEI Relatório:", _dtype="int"),
    "reserva_de_instrumentos": SimpleField(
        597, "Reserva de instrumentos:", True, True, True
    ),
    "sanada_ou_mitigada": FieldWithOptions(
        163, "Sanada ou mitigada?", mandatory=True, options=["", "0", "1"]
    ),
    "servicos_da_inspecao": FieldWithOptions(
        57,
        "Serviços da Inspeção:",
        mandatory=True,
        multiple=True,
        options=list(SERVICOS.values()),
        format_value=True,
    ),
    "situacao_constatada": FieldWithOptions(
        62,
        "Situação constatada:",
        mandatory=True,
        options=["", "Regular", "Irregular", "Inconclusivo", "Não analisado"],
    ),
    "situacao_de_risco_a_vida": FieldWithOptions(
        150,
        "Situação de risco à vida?",
        mandatory=True,
        options=["", "Não", "Sim"],
    ),
    "tipificacao_da_infracao": FieldWithOptions(
        148,
        "Tipificação da infração:",
        options=[
            "",
            "art. 163 da LGT – uso de RF",
            "art.  131 da LGT – exploração de serviço",
            "Outro",
        ],
    ),
    "tipo_de_fonte_interferente": FieldWithOptions(
        2068,
        "Tipo de fonte interferente:",
        mandatory=True,
        options=[
            "",
            "BSR",
            "Estação de Radiodifusão",
            "Estação de Telecomunicações",
            "Estação Clandestina",
            "Estação Estrangeira",
            "Reforçador de Celular",
            "Câmera sem fio",
            "Microfone sem fio",
            "Equipamento de Radiação Não Intencional",
            "Vazamento de TV a Cabo",
            "Rede Elétrica",
            "Outros",
        ],
    ),
    "tipo_de_inspecao": FieldWithOptions(
        2,
        "Tipo de inspeção:",
        mandatory=True,
        options=[
            "",
            "Bloqueio Administrativo",
            "Certificação",
            "Medição de CEMRF (RNI)",
            "Outorga - Aspectos não Técnicos",
            "Outorga - Aspectos Técnicos",
            "Uso do Espectro - Interferência",
            "Uso do Espectro - Monitoração",
            "Uso do Espectro - Não Outorgado",
        ],
        format_value=True,
        mapping={
            "Bloqueio Administrativo": [
                "observacao_tecnica_amostral",
                "utilizou_algum_instrumento",
                "utilizou_tecnicas_amostrais",
            ],
            "Certificação": [
                "area_do_pacp",
                "documento_instaurador_do_pado",
                "endereco_da_inspecao",
                "entidade_com_cadastro_stel",
                "houve_obice",
                "irregularidade",
                "latitude_coordenadas",
                "longitude_coordenadas",
                "no_sei_relatorio_de_atividades",
                "observacao_tecnica_amostral",
                "qnt_produt_lacradosapreend",
                "situacao_constatada",
                "utilizou_tecnicas_amostrais",
            ],
            "Medição de CEMRF (RNI)": [
                "campo_eletrico__pico_vm",
                "campo_eletrico_rms_vm",
                "entidade_da_inspecao",
                "entidade_outorgada",
                "frequencia_final",
                "frequencia_inicial",
                "latitude_coordenadas",
                "latitude_da_estacao",
                "longitude_coordenadas",
                "longitude_da_estacao",
                "observacao_tecnica_amostral",
                "tipo_de_medicao",
                "unidade_da_frequencia_final",
                "unidade_da_frequencia_inicial",
                "utilizou_tecnicas_amostrais",
            ],
            "Outorga - Aspectos não Técnicos": [
                "entidade_da_inspecao",
                "irregularidade",
                "observacao_tecnica_amostral",
                "pai_instaurado_pela_anatel",
                "situacao_constatada",
                "utilizou_tecnicas_amostrais",
            ],
            "Outorga - Aspectos Técnicos": [
                "altura_do_sistema_irradiante",
                "documento_instaurador_do_pado",
                "entidade_da_inspecao",
                "entidade_outorgada",
                "esta_em_operacao",
                "frequencias",
                "houve_interferencia",
                "houve_obice",
                "irregularidade",
                "latitude_coordenadas",
                "longitude_coordenadas",
                "observacao_tecnica_amostral",
                "potencia_medida",
                "situacao_constatada",
                "situacao_de_risco_a_vida",
                "unidade_de_frequencia",
                "unidade_de_potencia",
                "uso_de_produto_homologado",
                "utilizou_apoio_policial",
                "utilizou_tecnicas_amostrais",
            ],
            "Uso do Espectro - Interferência": [
                "entidade_da_inspecao",
                "foi_constatada_interferencia",
                "observacao_tecnica_amostral",
                "observacoes",
                "utilizou_tecnicas_amostrais",
            ],
            "Uso do Espectro - Monitoração": [
                "acao_de_risco_a_vida_criada",
                "entidade_da_inspecao",
                "frequencia_final",
                "frequencia_inicial",
                "latitude_coordenadas",
                "longitude_coordenadas",
                "no_sei_relatorio_de_atividades",
                "qtd_de_emissoes",
                "qtd_identificadas",
                "qtd_licenciadas",
                "unidade_da_frequencia_final",
                "unidade_da_frequencia_inicial",
            ],
            "Uso do Espectro - Não Outorgado": [
                "entidade_com_cadastro_stel",
                "frequencias",
                "houve_interferencia",
                "identificacao_da_nao_outorgada",
                "irregularidade",
                "latitude_coordenadas",
                "longitude_coordenadas",
                "observacao_tecnica_amostral",
                "potencia_medida",
                "qnt_produt_lacradosapreend",
                "situacao_constatada",
                "situacao_de_risco_a_vida",
                "tipificacao_da_infracao",
                "unidade_de_frequencia",
                "unidade_de_potencia",
                "uso_de_produto_homologado",
                "utilizou_apoio_policial",
                "utilizou_tecnicas_amostrais",
            ],
        },
    ),
    "tipo_de_medicao": FieldWithOptions(
        193, "Tipo de medição:", options=["", "Móvel", "Fixa", "Portátil"]
    ),
    "tipo_do_processo_plai": FieldWithOptions(
        426,
        "Tipo do PLAI:",
        options=[
            "",
            "Gestão da Fiscalização: Lacração, Apreensão e Interrupção",
            "Gestão da Fiscalização: Processo de Guarda",
        ],
    ),
    "ufmunicipio": FieldWithOptions(
        31,
        "UF/Município:",
        mandatory=True,
        multiple=True,
        options=MUNICIPIOS,
        format_value=True,
    ),
    "unidade_da_frequencia_final": FieldWithOptions(
        159,
        "Unidade (Frequência final):",
        mandatory=True,
        options=["", "Hz", "kHz", "MHz", "GHz", "THz"],
    ),
    "unidade_da_frequencia_inicial": FieldWithOptions(
        157,
        "Unidade (Frequência inicial):",
        mandatory=True,
        options=["", "Hz", "kHz", "MHz", "GHz", "THz"],
    ),
    "unidade_de_frequencia": FieldWithOptions(
        84,
        "Unidade (Frequência):",
        mandatory=False,
        options=["", "Hz", "kHz", "MHz", "GHz", "THz"],
    ),
    "unidade_de_potencia": FieldWithOptions(
        82,
        "Unidade (Potência):",
        mandatory=False,
        options=["", "mW", "W", "kW", "MW", "TW", "dBW", "dBm"],
    ),
    "uso_de_produto_homologado": FieldWithOptions(
        132,
        "Uso de produto homologado?",
        mandatory=True,
        options=["", "0", "1"],
        mapping={"1": ["no_de_homologacao"]},
    ),
    "utilizou_algum_instrumento": FieldWithOptions(
        598,
        "Utilizou algum instrumento?",
        mandatory=True,
        options=["", "0", "1"],
        mapping={"1": ["instrumentos_utilizados", "copiar_instrumento_da_reserva"]},
    ),
    "utilizou_apoio_policial": FieldWithOptions(
        75,
        "Utilizou apoio policial?",
        mandatory=True,
        options=["", "Nenhum", "Polícia Civil", "Polícia Militar", "Polícia Federal"],
    ),
    "utilizou_tecnicas_amostrais": FieldWithOptions(
        692,
        "Utilizou técnicas amostrais?",
        mandatory=True,
        options=["", "Usou técnicas amostrais", "Não usou técnicas amostrais"],
    ),
}