from constants import MUNICIPIOS, SERVICOS

ALL = {"status": "", "description": "", "start_date": "", "due_date": ""}

HIDDEN = {
    "gerar_plai": {
        "id": 426,
        "name": "Gerar PLAI",
        "tipo_processo": {
            "Gestão da Fiscalização: Lacração, Apreensão e Interrupção": "100000539",
            "Gestão da Fiscalização: Processo de Guarda": "100000618",
        },
        "replace_colon": True,
        "value": {"criar_processo": "", "tipo_processo": "", "coord_fi": ""},
    }
}


TECNICA = [
    "agrupamento",
    "ano_de_execucao",
    "app_fiscaliza",
    "classe_da_inspecao",
    "coordenacao_responsavel",
    "data_de_inicio_efetivo",
    "entidade_da_inspecao",
    "fiscais",
    "fiscal_responsavel",
    "horas_de_conclusao",
    "horas_de_deslocamento",
    "horas_de_execucao",
    "horas_de_preparacao",
    "no_pcdp",
    "no_sav",
    "no_sei_processo_fiscalizacao",
    "precisa_reservar_instrumentos",
    "procedimentos",
    "servicos_da_inspecao",
    "subtema",
    "tema",
    "tipo_de_inspecao",
    "total_de_horas",
    "ufmunicipio",
    "utilizou_algum_instrumento",
]

FIELDS = {
    "acao_de_risco_a_vida_criada": {
        "id": 154,
        "name": "Ação de risco à vida criada?",
        "value": "",
    },
    "agrupamento": {"id": 213, "name": "Agrupamento", "value": ""},
    "altura_do_sistema_irradiante": {
        "id": 131,
        "name": "Altura do sistema irradiante",
        "value": "",
    },
    "ano_de_execucao": {"id": 5, "name": "Ano de Execução", "value": ""},
    "app_fiscaliza": {"id": 463, "name": "App Fiscaliza", "value": ""},
    "area_do_pacp": {
        "id": 416,
        "name": "Área do PACP",
        "options": [
            "1-Comércio",
            "2-ISP",
            "3-E-commerce",
            "4-Aduana",
            "5-Feiras e Eventos",
            "6-Supervisão de Mercados",
        ],
        "value": {"texto": "", "valor": ""},
    },
    "campo_eletrico__pico_vm": {
        "id": 195,
        "name": "Campo elétrico - pico (V/m)",
        "value": "",
    },
    "campo_eletrico_rms_vm": {
        "id": 194,
        "name": "Campo elétrico RMS (V/m)",
        "value": "",
    },
    "classe_da_inspecao": {
        "id": 89,
        "name": "Classe da Inspeção",
        "value": {"valor": "", "texto": ""},
    },
    "cnpjcpf_da_entidade": {"id": 141, "name": "CNPJ/CPF da Entidade", "value": ""},
    "coordenacao_responsavel": {
        "id": 178,
        "name": "Coordenação responsável",
        "value": "",
    },
    "coordenadas_estacao": {"id": 718, "name": "Coordenadas Estação", "value": ""},
    "coordenadas_geograficas": {
        "id": 717,
        "name": "Coordenadas Geográficas",
        "replace_colon": True,
        "value": {"latitude": "", "longitude": ""},
    },
    "copiar_instrumento_da_reserva": {
        "id": 629,
        "name": "Copiar instrumento da reserva?",
        "options": ["0", "1"],
        "value": "",
    },
    "dadospacp": {"id": 415, "name": "DadosPACP", "value": ""},
    "data_de_inicio_efetivo": {
        "id": 627,
        "name": "Data de início efetivo",
        "value": "",
    },
    "documento_instaurador_do_pado": {
        "id": 134,
        "name": "Documento instaurador do PADO",
        "value": "",
    },
    "endereco_da_inspecao": {"id": 142, "name": "Endereço da Inspeção", "value": ""},
    "entidade_com_cadastro_stel": {
        "id": 189,
        "name": "Entidade com cadastro STEL?",
        "mandatory": True,
        "options": ["Sim", "Não"],
        "value": "",
    },
    "entidade_da_inspecao": {
        "id": 30,
        "name": "Entidade da Inspeção",
        "multiple": True,
        "value": [""],
    },
    "entidade_outorgada": {
        "id": 138,
        "name": "Entidade outorgada?",
        "values": {"1": {"mandatory": ["numero_da_estacao"]}, "0": {}},
        "value": "",
    },
    "esta_em_operacao": {
        "id": 139,
        "name": "Está em operação?",
        "options": ["1", "0"],
        "value": "",
    },
    "fiscais": {
        "id": 26,
        "name": "Fiscais",
        "mandatory": True,
        "multiple": True,
        "value": [""],
    },
    "fiscal_responsavel": {
        "id": 25,
        "name": "Fiscal responsável",
        "mandatory": True,
        "value": "",
    },
    "foi_constatada_interferencia": {
        "id": 1967,
        "name": "Foi constatada interferência?",
        "value": "",
    },
    "frequencia_final": {"id": 158, "name": "Frequência final", "value": "20"},
    "frequencia_inicial": {"id": 156, "name": "Frequência inicial", "value": "10"},
    "frequencias": {"id": 180, "name": "Frequência(s)", "value": ""},
    "horas_de_conclusao": {
        "id": 94,
        "name": "Horas de conclusão",
        "mandatory": True,
        "value": "",
    },
    "horas_de_deslocamento": {
        "id": 92,
        "name": "Horas de Deslocamento",
        "mandatory": True,
        "value": "",
    },
    "horas_de_execucao": {
        "id": 93,
        "name": "Horas de Execução",
        "mandatory": True,
        "value": "",
    },
    "horas_de_preparacao": {
        "id": 91,
        "name": "Horas de Preparação",
        "mandatory": True,
        "value": "",
    },
    "houve_interferencia": {"id": 149, "name": "Houve interferência?", "value": ""},
    "houve_obice": {
        "id": 136,
        "name": "Houve óbice?",
        "mandatory": True,
        "options": ["Sim", "Não"],
        "value": "",
    },
    "identificacao_da_nao_outorgada": {
        "id": 250,
        "name": "Identificação da não Outorgada",
        "value": "",
    },
    "instrumentos_utilizados": {
        "id": 599,
        "name": "Instrumentos Utilizados",
        "mandatory": True,
        "value": "",
    },
    "irregularidade": {
        "id": 73,
        "name": "Irregularidade",
        "multiple": True,
        "options": [
            "Comercialização de produtos",
            "Utilização de produtos",
            "Conteúdo",
            "Outros aspectos não técnicos",
            "Recursos de acessibilidade",
        ],
        "value": [{"valor": "", "texto": ""}],
    },
    "lai_vinculadas": {"id": 481, "name": "LAI vinculadas", "value": ""},
    "latitude_coordenadas": {"id": 170, "name": "Latitude (coordenadas)", "value": ""},
    "latitude_da_estacao": {"id": 191, "name": "Latitude da estação", "value": ""},
    "longitude_coordenadas": {
        "id": 171,
        "name": "Longitude (coordenadas)",
        "value": "",
    },
    "longitude_da_estacao": {"id": 192, "name": "Longitude da estação", "value": ""},
    "motivo_de_lai": {
        "id": 164,
        "multiple": True,
        "options": [
            "Risco à vida",
            "Clandestinidade",
            "Interferência prejudicial",
            "Uso de produto não certificado",
            " Garantir a segurança (exposição a campos eletromagnéticos)",
            " Necessidade de assegurar o planejamento, o gerenciamento e a coordenação do uso de espectro de radiofrequências (justificar)",
        ],
        "name": "Motivo de LAI",
        "value": [""],
    },
    "numero_da_estacao": {"id": 137, "name": "Número da estação", "value": ""},
    "no_de_homologacao": {"id": 161, "name": "Nº de homologação", "value": ""},
    "no_do_lacre": {"id": 165, "name": "Nº do lacre", "value": ""},
    "no_pcdp": {"id": 112, "name": "Nº PCDP", "value": ""},
    "no_sav": {"id": 111, "name": "Nº SAV", "value": ""},
    "no_sei_do_aviso_lai": {
        "id": 427,
        "name": "Nº SEI do Aviso LAI",
        "replace_colon": True,
        "value": {"numero": ""},
    },
    "no_sei_do_plaiguarda": {
        "id": 426,
        "name": "Nº SEI do PLAI/Guarda",
        "replace_colon": True,
        "value": {"numero": ""},
    },
    "no_sei_processo_fiscalizacao": {
        "id": 422,
        "name": "Nº SEI Processo Fiscalização",
        "mandatory": True,
        "replace_colon": True,
        "value": {"numero": ""},
    },
    "no_sei_relatorio_monitoramento": {
        "id": 544,
        "name": "Nº SEI Relatório Monitoramento",
        "value": "",
    },
    "nome_da_entidade": {
        "id": 140,
        "name": "Nome da Entidade",
        "mandatory": True,
        "value": "",
    },
    "observacao_tecnica_amostral": {
        "id": 693,
        "name": "Observação (técnica amostral)",
        "value": "",
    },
    "observacoes": {"id": 1973, "name": "Observações", "value": ""},
    "pai_instaurado_pela_anatel": {
        "id": 160,
        "name": "PAI instaurado pela Anatel?",
        "value": "",
    },
    "potencia_medida": {"id": 81, "name": "Potência medida", "value": ""},
    "precisa_reservar_instrumentos": {
        "id": 596,
        "name": "Precisa reservar instrumentos?",
        "mandatory": True,
        "map": {"1": {"mandatory": ["reserva_de_instrumentos"]}, "0": {}},
        "value": "",
    },
    "procedimentos": {
        "id": 71,
        "name": "Procedimentos",
        "multiple": True,
        "map": {
            "Nenhum": {},
            "Lacração": {
                "mandatory": ["no_do_lacre", "motivo_de_lai", "no_sei_do_aviso_lai"],
                "optional": ["lai_vinculadas", "no_sei_do_plaiguarda", "gerar_plai"],
            },
            "Apreensão": {
                "mandatory": ["motivo_de_lai", "no_sei_do_aviso_lai"],
                "optional": ["lai_vinculadas", "no_sei_do_plaiguarda", "gerar_plai"],
            },
            "Interrupção": {
                "mandatory": ["motivo_de_lai", "no_sei_do_aviso_lai"],
                "optional": ["lai_vinculadas", "no_sei_do_plaiguarda", "gerar_plai"],
            },
            "Não Cadastrado": {},
            "Notificado": {},
            "A Notificar": {},
            "Liberação/Desinterrupção": {},
            "Orientação ao Usuário": {},
            "Comunicado": {},
            "Deslacrado": {},
            "Vistoriado": {},
            "Emissão Termo Violação de Lacre": {},
            "Apoio a busca e apreensão": {},
            "Investigação/Pesquisa": {},
            "Não Lacrado - Impedimento": {},
            "Não Lacrado - Amparo Judicial": {},
            "Não Lacrado - Responsável Ausente": {},
            "Não Lacrado - Local Fechado": {},
            "Constatação Violação Lacre/Relacrado": {},
            "Constatação Violação Lacre/Impedimento": {},
            "Notícia Crime": {},
            "Monitorado alterado": {},
            "Constatação Encerramento - Informe": {},
            "Levantamento de Dados": {},
            "Análise/coleta de Dados": {},
            "Monitorado": {},
            "Não Lacrado - Desativado": {},
            "Devolução de Produto(s)": {},
        },
        "value": [],
    },
    "qnt_produt_lacradosapreend": {
        "id": 143,
        "name": "Qnt. produt. lacrados/apreend.",
        "value": "",
    },
    "qtd_de_emissoes": {"id": 69, "name": "Qtd. de Emissões", "value": ""},
    "qtd_identificadas": {"id": 731, "name": "Qtd. Identificadas", "value": ""},
    "qtd_licenciadas": {"id": 730, "name": "Qtd. Licenciadas", "value": ""},
    "reserva_de_instrumentos": {
        "id": 597,
        "multiple": True,
        "name": "Reserva de instrumentos",
        "mandatory": True,
        "value": [{"id": "", "valor": "", "texto": ""}],
    },
    "servicos_da_inspecao": {
        "id": 57,
        "name": "Serviços da Inspeção",
        "multiple": True,
        "options": SERVICOS,
        "value": [{"valor": "", "texto": ""}],
    },
    "situacao_constatada": {
        "id": 62,
        "name": "Situação constatada",
        "mandatory": True,
        "options": ["Regular", "Irregular", "Inconclusivo", "Não analisado"],
        "value": "",
    },
    "situacao_de_risco_a_vida": {
        "id": 150,
        "name": "Situação de risco à vida?",
        "value": {"valor": "", "texto": ""},
    },
    "subtema": {
        "id": 15,
        "name": "Subtema",
        "multiple": True,
        "value": [{"valor": "", "texto": ""}],
    },
    "tema": {
        "id": 14,
        "name": "Tema",
        "multiple": True,
        "value": [{"valor": "", "texto": ""}],
    },
    "tipificacao_da_infracao": {
        "id": 148,
        "name": "Tipificação da infração",
        "value": "",
    },
    "tipo_de_inspecao": {
        "id": 2,
        "name": "Tipo de inspeção",
        "mandatory": True,
        "map": {
            "Bloqueio Administrativo": {
                "mandatory": [
                    "nome_da_entidade",
                    "observacao_tecnica_amostral",
                    "utilizou_algum_instrumento",
                    "utilizou_tecnicas_amostrais",
                ],
                "optional": [],
            },
            "Certificação": {
                "mandatory": [
                    "endereco_da_inspecao",
                    "entidade_com_cadastro_stel",
                    "houve_obice",
                    "latitude_coordenadas",
                    "longitude_coordenadas",
                    "nome_da_entidade",
                    "observacao_tecnica_amostral",
                    "qnt_produt_lacradosapreend",
                    "situacao_constatada",
                    "utilizou_tecnicas_amostrais",
                ],
                "optional": [
                    "area_do_pacp",
                    "cnpjcpf_da_entidade",
                    "documento_instaurador_do_pado",
                    "irregularidade",
                ],
            },
            "Medição de CEMRF (RNI)": {
                "mandatory": [
                    "campo_eletrico__pico_vm",
                    "campo_eletrico_rms_vm",
                    "coordenadas_estacao",
                    "coordenadas_geograficas",
                    "entidade_outorgada",
                    "frequencia_final",
                    "frequencia_inicial",
                    "latitude_coordenadas",
                    "latitude_da_estacao",
                    "longitude_coordenadas",
                    "longitude_da_estacao",
                    "nome_da_entidade" "observacao_tecnica_amostral",
                    "tipo_de_medicao",
                    "servicos_da_inspecao",
                    "unidade_da_frequencia_final",
                    "unidade_da_frequencia_inicial",
                    "utilizou_tecnicas_amostrais",
                ],
                "optional": ["cnpjcpf_da_entidade"],
            },
            "Outorga - Aspectos não Técnicos": {
                "mandatory": [
                    "irregularidade",
                    "observacao_tecnica_amostral",
                    "pai_instaurado_pela_anatel",
                    "servicos_da_inspecao",
                    "situacao_constatada",
                    "utilizou_tecnicas_amostrais",
                ],
                "optional": ["cnpjcpf_da_entidade"],
            },
            "Outorga - Aspectos Técnicos": {
                "mandatory": [
                    "altura_do_sistema_irradiante",
                    # "coordenadas_geograficas",
                    "documento_instaurador_do_pado",
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
                "optional": [],
            },
            "Uso do Espectro - Interferência": {
                "mandatory": [
                    "utilizou_tecnicas_amostrais",
                    "observacao_tecnica_amostral",
                    "foi_constatada_interferencia",
                    "observacoes",
                ],
                "optional": [],
            },
            "Uso do Espectro - Monitoração": {
                "mandatory": [
                    "qtd_de_emissoes",
                    "qtd_licenciadas",
                    "qtd_identificadas",
                    "latitude_coordenadas",
                    "longitude_coordenadas",
                    "acao_de_risco_a_vida_criada",
                    "frequencia_inicial",
                    "unidade_da_frequencia_inicial",
                    "frequencia_final",
                    "unidade_da_frequencia_final",
                    "no_sei_relatorio_monitoramento",
                    "coordenadas_geograficas",
                ],
                "optional": [],
            },
            "Uso do Espectro - Não Outorgado": {
                "mandatory": [
                    "entidade_com_cadastro_stel",
                    "uso_de_produto_homologado",
                    "situacao_constatada",
                    "irregularidade",
                    "potencia_medida",
                    "unidade_de_potencia",
                    "frequencias",
                    "unidade_de_frequencia",
                    "utilizou_apoio_policial",
                    "qnt_produt_lacradosapreend",
                    "tipificacao_da_infracao",
                    "houve_interferencia",
                    "situacao_de_risco_a_vida",
                    "latitude_coordenadas",
                    "longitude_coordenadas",
                    "identificacao_da_nao_outorgada",
                    "utilizou_tecnicas_amostrais",
                    "observacao_tecnica_amostral",
                    "coordenadas_geograficas",
                ],
                "optional": [],
            },
        },
        "value": {"valor": "", "texto": ""},
    },
    "tipo_de_medicao": {"id": 193, "name": "Tipo de medição", "value": ""},
    "tipo_do_processo_plai": {
        "id": 426,
        "name": "Tipo do Processo PLAI",
        "options": [
            "Gestão da Fiscalização: Lacração, Apreensão e Interrupção",
            "Gestão da Fiscalização: Processo de Guarda",
        ],
        "value": "",
    },
    "total_de_horas": {"id": 1789, "name": "Total de horas", "value": ""},
    "ufmunicipio": {
        "id": 31,
        "name": "UF/Município",
        "mandatory": True,
        "multiple": True,
        "options": MUNICIPIOS,
        "value": [{"valor": "", "texto": ""}],
    },
    "unidade_da_frequencia_final": {
        "id": 159,
        "name": "Unidade da frequência final",
        "value": "MHz",
    },
    "unidade_da_frequencia_inicial": {
        "id": 157,
        "name": "Unidade da frequência inicial",
        "value": "MHz",
    },
    "unidade_de_frequencia": {"id": 84, "name": "Unidade de Frequência", "value": ""},
    "unidade_de_potencia": {"id": 82, "name": "Unidade de Potência", "value": ""},
    "uso_de_produto_homologado": {
        "id": 132,
        "name": "Uso de produto homologado?",
        "map": {"1": {"optional": ["no_de_homologacao"]}, "0": {}},
        "value": "",
    },
    "utilizou_algum_instrumento": {
        "id": 598,
        "name": "Utilizou algum instrumento?",
        "mandatory": True,
        "map": {
            "1": {
                "mandatory": ["instrumentos_utilizados"],
                "optional": ["copiar_instrumento_da_reserva"],
            },
            "0": {},
        },
        "value": "",
    },
    "utilizou_apoio_policial": {
        "id": 75,
        "name": "Utilizou apoio policial?",
        "value": "",
    },
    "utilizou_tecnicas_amostrais": {
        "id": 692,
        "name": "Utilizou técnicas amostrais?",
        "mandatory": True,
        "options": ["Usou técnicas amostrais", "Não usou técnicas amostrais"],
        "value": "",
    },
}
