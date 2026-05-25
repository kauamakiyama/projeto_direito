"""
Base de jurisprudência consolidada para análise jurimétrica.
Cobre os tipos de causa mais comuns no JEC.
"""

JURISPRUDENCIA_JEC = {
    "cobranca_indevida": {
        "gatilhos": [
            "cobrança indevida", "débito indevido", "negativação indevida",
            "protesto indevido", "inscrição indevida", "spc", "serasa",
            "banco", "cartão", "financeira", "crédito", "empréstimo",
            "bradesco", "itaú", "itau", "caixa econômica", "caixa economica",
            "santander", "nubank", "inter", "c6 bank", "picpay", "sicredi",
            "banco do brasil", "safra", "bmg", "pan", "sicoob",
            "cobrado indevidamente", "cobrança abusiva", "taxa indevida",
            "tarifa indevida", "juros abusivos", "anatocismo",
            "desconto não autorizado", "débito automático indevido",
        ],
        "estimativa_exito": "Alta — 75% a 85%",
        "fundamentos": [
            "Súmula 297 STJ: CDC aplica-se às instituições financeiras",
            "Art. 42 CDC: devolução em dobro do valor cobrado indevidamente",
            "Súmula 385 STJ: negativação indevida gera dano moral presumido",
            "Teoria do risco do empreendimento: responsabilidade objetiva do banco",
        ],
        "valor_tipico_dano_moral": "R$ 2.000 – R$ 5.000",
        "valor_tipico_material": "Devolução em dobro do valor cobrado",
        "fatores_positivos": [
            "prova do débito indevido",
            "notificação ignorada pela empresa",
            "negativação no SPC/Serasa",
        ],
        "fatores_negativos": [
            "débito preexistente legítimo",
            "confusão do próprio consumidor",
        ],
        "fonte": "Súmula 297 e 385 STJ · Art. 42 CDC · TJSP 2024",
    },

    "nao_entrega_produto": {
        "gatilhos": [
            "não entrega", "nao entrega", "atraso entrega", "atraso na entrega",
            "produto não recebido", "extravio", "e-commerce", "compra online",
            "loja virtual", "mercadoria", "compra e venda", "compra",
            "venda de produto", "marketplace", "mercado livre", "shopee",
            "amazon", "magazine luiza", "americanas", "casas bahia",
            "submarino", "extra", "carrefour", "aliexpress", "shein",
            "produto não chegou", "encomenda", "correios", "transportadora",
            "sedex", "pac", "jadlog", "loggi", "entrega não realizada",
            "pedido cancelado sem reembolso", "devolução negada",
        ],
        "estimativa_exito": "Alta — 70% a 80%",
        "fundamentos": [
            "Art. 35 CDC: direito de exigir entrega, aceitar substituto ou rescindir",
            "TJSP consolidado: não entrega em compra online gera dano moral presumido",
            "Art. 14 CDC: responsabilidade objetiva pelo defeito na prestação do serviço",
        ],
        "valor_tipico_dano_moral": "R$ 2.000 – R$ 5.000",
        "valor_tipico_material": "Restituição integral do valor pago",
        "fatores_positivos": [
            "comprovante de compra",
            "ausência de entrega documentada",
            "tentativas de contato sem resposta",
        ],
        "fatores_negativos": [
            "atraso menor que 7 dias",
            "produto entregue com defeito (causa diferente)",
        ],
        "fonte": "Art. 35 CDC · TJSP jurisprudência consolidada 2024",
    },

    "plano_saude_negativa": {
        "gatilhos": [
            "plano de saúde", "plano de saude", "convênio médico", "convenio medico",
            "negativa cobertura", "recusa procedimento", "operadora saúde",
            "operadora saude", "ans", "saúde suplementar", "saude suplementar",
            "unimed", "amil", "sulamerica", "sul america", "bradesco saúde",
            "bradesco saude", "porto seguro saúde", "hapvida", "notredame",
            "notre dame", "green line", "gndi", "prevent senior",
            "medicamento negado", "internação negada", "internacao negada",
            "cirurgia negada", "exame negado", "consulta negada",
            "tratamento negado", "procedimento negado", "home care",
            "quimioterapia", "radioterapia", "ortopedia", "psicologia",
            "psiquiatria", "fisioterapia", "cobertura negada",
        ],
        "estimativa_exito": "Muito alta — 80% a 90%",
        "fundamentos": [
            "Súmula 608 STJ: negativa de cobertura de urgência ou emergência gera dano moral",
            "Lei 9.656/98: rol de procedimentos obrigatórios da ANS",
            "STJ: cláusula limitativa de cobertura é abusiva quando não destacada",
            "Resolução ANS 465/2021: rol taxativo mas com abertura para analogia",
        ],
        "valor_tipico_dano_moral": "R$ 5.000 – R$ 15.000",
        "valor_tipico_material": "Custeio integral do procedimento negado",
        "fatores_positivos": [
            "urgência ou emergência comprovada",
            "procedimento no rol ANS",
            "prescrição médica documentada",
        ],
        "fatores_negativos": [
            "procedimento experimental",
            "procedimento estético",
            "carência contratual não cumprida",
        ],
        "fonte": "Súmula 608 STJ · Lei 9.656/98 · Resolução ANS 465/2021",
    },

    "fraude_bancaria": {
        "gatilhos": [
            "fraude", "cartão clonado", "saque indevido", "golpe",
            "phishing", "transferência não autorizada", "transferencia nao autorizada",
            "pix indevido", "clonagem", "estelionato", "crime virtual",
            "conta hackeada", "acesso não autorizado", "acesso nao autorizado",
            "golpe do pix", "engenharia social", "falso funcionário",
            "falso funcionario", "maquininha", "golpe whatsapp",
            "compra não reconhecida", "compra nao reconhecida",
            "transação não reconhecida", "transacao nao reconhecida",
            "débito não autorizado", "debito nao autorizado",
        ],
        "estimativa_exito": "Alta — 70% a 80%",
        "fundamentos": [
            "Súmula 479 STJ: bancos respondem de forma objetiva por fraudes de terceiros",
            "Art. 14 CDC: defeito na prestação do serviço de segurança",
            "STJ: risco do empreendimento bancário não pode ser transferido ao consumidor",
        ],
        "valor_tipico_dano_moral": "R$ 3.000 – R$ 8.000",
        "valor_tipico_material": "Restituição integral do valor fraudado",
        "fatores_positivos": [
            "boletim de ocorrência registrado",
            "contestação imediata ao banco",
            "ausência de compartilhamento de senha",
        ],
        "fatores_negativos": [
            "compartilhamento de senha comprovado",
            "demora superior a 90 dias para contestar",
        ],
        "fonte": "Súmula 479 STJ · Art. 14 CDC",
    },

    "rescisao_contrato_telecom": {
        "gatilhos": [
            "telefonia", "internet", "cancelamento", "rescisão", "rescisao",
            "multa fidelidade", "serviço não prestado", "servico nao prestado",
            "claro", "vivo", "tim", "oi", "net", "anatel",
            "sky", "embratel", "nextel", "brisanet", "algar",
            "fibra óptica", "fibra optica", "banda larga", "wi-fi",
            "sinal ruim", "serviço interrompido", "servico interrompido",
            "queda de sinal", "velocidade inferior", "internet lenta",
            "fidelização abusiva", "fidelizacao abusiva",
            "cobrança após cancelamento", "cobranca apos cancelamento",
            "portabilidade", "número portado", "numero portado",
        ],
        "estimativa_exito": "Média-alta — 60% a 75%",
        "fundamentos": [
            "Art. 51 CDC: cláusulas abusivas são nulas de pleno direito",
            "Resolução Anatel 632/2014: multa de fidelidade proporcional ao tempo restante",
            "TJSP: cobrança após cancelamento gera dano moral",
            "Anatel: direito de cancelamento sem multa após 12 meses de contrato",
        ],
        "valor_tipico_dano_moral": "R$ 1.000 – R$ 3.000",
        "valor_tipico_material": "Devolução da multa cobrada indevidamente",
        "fatores_positivos": [
            "protocolo de cancelamento documentado",
            "cobrança após cancelamento",
            "serviço não prestado como contratado",
        ],
        "fatores_negativos": [
            "cancelamento dentro da fidelidade sem justificativa",
            "ausência de protocolo de cancelamento",
        ],
        "fonte": "Art. 51 CDC · Resolução Anatel 632/2014 · TJSP 2024",
    },

    "produto_com_defeito": {
        "gatilhos": [
            "produto com defeito", "vício oculto", "vicio oculto", "garantia",
            "produto defeituoso", "mal funcionamento", "produto parou de funcionar",
            "vício do produto", "vicio do produto", "eletrodoméstico", "eletrodomestico",
            "celular", "smartphone", "notebook", "computador", "televisão", "televisao",
            "tv", "geladeira", "refrigerador", "máquina de lavar", "maquina de lavar",
            "ar condicionado", "micro-ondas", "microondas", "fogão", "fogao",
            "lava-louça", "lava-loucas", "aspirador", "liquidificador",
            "produto com vício", "produto com vicio", "assistência técnica",
            "assistencia tecnica", "reparo negado", "substituição negada",
            "substituicao negada", "fora de garantia contestado",
        ],
        "estimativa_exito": "Alta — 70% a 80%",
        "fundamentos": [
            "Art. 18 CDC: fornecedor responde por vícios de qualidade do produto",
            "Art. 26 CDC: prazo decadencial de 90 dias para bens duráveis",
            "CDC: direito de reparo, substituição, abatimento ou devolução",
            "TJSP: vício oculto em produto durável gera dano moral quando há descaso",
        ],
        "valor_tipico_dano_moral": "R$ 1.000 – R$ 4.000 (se houver descaso)",
        "valor_tipico_material": "Reparo, substituição ou devolução do valor",
        "fatores_positivos": [
            "produto dentro da garantia",
            "nota fiscal",
            "registro de reclamação na assistência técnica",
        ],
        "fatores_negativos": [
            "produto fora da garantia",
            "mau uso comprovado",
            "ausência de nota fiscal",
        ],
        "fonte": "Arts. 18 e 26 CDC · TJSP 2024",
    },

    "transporte_aereo": {
        "gatilhos": [
            "voo", "atraso de voo", "cancelamento de voo", "voo cancelado",
            "voo atrasado", "overbooking", "preterição de embarque",
            "extravio de bagagem", "bagagem extraviada", "bagagem danificada",
            "mala perdida", "companhia aérea", "companhia aerea",
            "latam", "gol", "azul", "avianca", "passagem aérea", "passagem aerea",
            "remarcação forçada", "remarcacao forcada", "conexão perdida",
            "conexao perdida", "escala perdida", "embarque negado",
            "reembolso passagem", "milhas", "programa fidelidade",
        ],
        "estimativa_exito": "Alta — 75% a 85%",
        "fundamentos": [
            "Convenção de Montreal: responsabilidade objetiva da companhia aérea",
            "Art. 14 CDC: responsabilidade pelo defeito na prestação do serviço",
            "TJSP e STJ: atraso superior a 4h gera dano moral presumido",
            "ANAC Resolução 400/2016: direitos do passageiro em caso de atraso e cancelamento",
        ],
        "valor_tipico_dano_moral": "R$ 3.000 – R$ 10.000",
        "valor_tipico_material": "Reembolso integral da passagem + despesas comprovadas",
        "fatores_positivos": [
            "atraso superior a 4 horas documentado",
            "ausência de assistência pela companhia (alimentação, hotel)",
            "bagagem extraviada com lista de itens",
            "despesas extras comprovadas por recibo",
        ],
        "fatores_negativos": [
            "atraso por caso fortuito ou força maior (clima extremo)",
            "ausência de documentação das despesas extras",
            "atraso inferior a 1 hora",
        ],
        "fonte": "Convenção de Montreal · ANAC Res. 400/2016 · STJ · TJSP 2024",
    },

    "seguro_negado": {
        "gatilhos": [
            "seguro", "sinistro", "sinistro negado", "cobertura negada",
            "seguro auto", "seguro automóvel", "seguro automovel",
            "seguro residencial", "seguro de vida", "seguro viagem",
            "porto seguro", "suhai", "hdi", "tokio marine", "allianz",
            "liberty", "mapfre", "azul seguros", "bb seguridade",
            "bradesco seguros", "itaú seguros", "itau seguros",
            "recusa de sinistro", "franquia", "indenização negada",
            "indenizacao negada", "perda total", "roubo de veículo",
            "roubo de veiculo", "furto do veículo", "furto do veiculo",
            "acidente não coberto", "acidente nao coberto",
        ],
        "estimativa_exito": "Média-alta — 60% a 75%",
        "fundamentos": [
            "Art. 757 CC: obrigação do segurador de indenizar o sinistro coberto",
            "Art. 51 CDC: cláusulas excludentes abusivas são nulas",
            "STJ: interpretação favorável ao segurado em caso de dúvida (in dubio pro segurado)",
            "TJSP: exclusão de cobertura deve ser previamente informada de forma clara",
        ],
        "valor_tipico_dano_moral": "R$ 3.000 – R$ 8.000",
        "valor_tipico_material": "Valor integral da indenização prevista na apólice",
        "fatores_positivos": [
            "apólice vigente na data do sinistro",
            "boletim de ocorrência registrado",
            "sinistro enquadrado na cobertura contratada",
            "prêmio pago em dia",
        ],
        "fatores_negativos": [
            "exclusão de cobertura clara e informada previamente",
            "fraude comprovada",
            "carência não cumprida",
            "sinistro por embriaguez",
        ],
        "fonte": "Art. 757 CC · Art. 51 CDC · STJ · TJSP 2024",
    },

    "veiculo_defeito": {
        "gatilhos": [
            "veículo", "veiculo", "carro", "automóvel", "automovel",
            "moto", "motocicleta", "concessionária", "concessionaria",
            "recall", "defeito de fábrica", "defeito de fabrica",
            "vício redibitório", "vicio redibitori", "revisão", "revisao",
            "garantia veículo", "garantia veiculo", "fipe", "tabela fipe",
            "carro usado", "carro seminovo", "vícios ocultos veículo",
            "honda", "toyota", "volkswagen", "vw", "chevrolet", "gm",
            "fiat", "ford", "hyundai", "jeep", "renault", "nissan",
            "mitsubishi", "subaru", "volvo", "mercedes", "bmw", "audi",
            "motor fundido", "câmbio", "cambio", "suspensão", "suspensao",
            "freio", "air bag", "airbag", "compra de veículo", "compra de veiculo",
        ],
        "estimativa_exito": "Média-alta — 60% a 75%",
        "fundamentos": [
            "Art. 18 CDC: responsabilidade por vícios de qualidade",
            "Art. 26 CDC: prazo decadencial de 90 dias para bens duráveis",
            "STJ: vício oculto em veículo usado gera responsabilidade solidária",
            "TJSP: recall não realizado gera responsabilidade da montadora",
        ],
        "valor_tipico_dano_moral": "R$ 3.000 – R$ 8.000",
        "valor_tipico_material": "Reparo gratuito, substituição ou restituição do valor",
        "fatores_positivos": [
            "defeito dentro do prazo de garantia",
            "nota fiscal de compra",
            "laudo técnico comprovando o defeito",
            "reclamações anteriores na concessionária documentadas",
        ],
        "fatores_negativos": [
            "veículo com manutenção inadequada comprovada",
            "modificações não autorizadas",
            "veículo fora da garantia sem vício oculto caracterizado",
        ],
        "fonte": "Arts. 18 e 26 CDC · STJ · TJSP 2024",
    },

    "servico_mal_prestado": {
        "gatilhos": [
            "serviço mal prestado", "servico mal prestado",
            "obra", "reforma", "construção", "construcao", "pintura",
            "instalação", "instalacao", "manutenção", "manutencao",
            "prestador de serviço", "prestador de servico",
            "empreiteira", "pedreiro", "encanador", "eletricista",
            "serviço não concluído", "servico nao concluido",
            "serviço entregue com defeito", "serviço entregue incorreto",
            "escola", "curso", "faculdade", "mensalidade", "bolsa",
            "academia", "estética", "estetica", "salão", "salao",
            "clínica", "clinica", "dentista", "médico particular",
            "medico particular", "hospital particular",
            "serviço não prestado", "servico nao prestado",
            "contrato de prestação de serviços",
        ],
        "estimativa_exito": "Média — 55% a 70%",
        "fundamentos": [
            "Art. 20 CDC: o fornecedor responde por vícios na prestação de serviço",
            "Art. 14 CDC: responsabilidade objetiva pelo defeito no serviço",
            "CDC: direito de reexecução, abatimento ou restituição do valor pago",
            "CC Art. 389: inadimplemento contratual gera obrigação de indenizar",
        ],
        "valor_tipico_dano_moral": "R$ 1.000 – R$ 5.000 (se houver descaso ou dano)",
        "valor_tipico_material": "Restituição do valor pago ou custo de correção",
        "fatores_positivos": [
            "contrato escrito com escopo definido",
            "fotos/vídeos documentando o defeito",
            "orçamento de terceiro para corrigir o serviço",
            "notificação prévia ao prestador",
        ],
        "fatores_negativos": [
            "contrato verbal sem provas",
            "pagamento integral antes da entrega",
            "ausência de documentação do defeito",
        ],
        "fonte": "Arts. 14 e 20 CDC · CC Art. 389 · TJSP 2024",
    },

    "acidente_transito": {
        "gatilhos": [
            "acidente de trânsito", "acidente de transito", "colisão", "colisao",
            "batida", "acidente", "atropelamento", "danos ao veículo",
            "danos ao veiculo", "indenização por acidente", "indenizacao por acidente",
            "culpa no acidente", "boletim de ocorrência", "dpvat", "seguro dpvat",
            "seguro obrigatório", "responsabilidade civil", "danos materiais acidente",
            "danos morais acidente", "lesão corporal", "lesao corporal",
            "invalidez", "incapacidade", "pensão por acidente", "pensao por acidente",
        ],
        "estimativa_exito": "Média — 55% a 70%",
        "fundamentos": [
            "Art. 186 CC: ato ilícito que causa dano gera obrigação de indenizar",
            "Art. 927 CC: responsabilidade civil por dano causado",
            "CTB: presunção de culpa em determinadas situações de trânsito",
            "STJ: dano moral in re ipsa em casos de lesão corporal grave",
        ],
        "valor_tipico_dano_moral": "R$ 3.000 – R$ 15.000 (conforme gravidade)",
        "valor_tipico_material": "Reparação integral do veículo ou valor de mercado + lucros cessantes",
        "fatores_positivos": [
            "boletim de ocorrência lavrado na hora",
            "testemunhas identificadas",
            "laudos médicos (se houver lesão)",
            "fotos do local e dos veículos",
        ],
        "fatores_negativos": [
            "culpa concorrente da vítima",
            "ausência de boletim de ocorrência",
            "ausência de testemunhas",
        ],
        "fonte": "Arts. 186 e 927 CC · CTB · STJ · TJSP 2024",
    },

    "generico": {
        "gatilhos": [],
        "estimativa_exito": "Não foi possível estimar com precisão",
        "fundamentos": [
            "Análise baseada nos princípios gerais do CDC e jurisprudência do STJ",
        ],
        "valor_tipico_dano_moral": "Variável conforme o caso",
        "valor_tipico_material": "Variável conforme o caso",
        "fatores_positivos": [
            "documentação completa",
            "tentativa prévia de resolução extrajudicial",
        ],
        "fatores_negativos": [
            "ausência de provas documentais",
        ],
        "fonte": "CDC · STJ · jurisprudência consolidada",
    },
}


def _texto_partes(partes):
    if not partes:
        return ""
    nomes = []
    for p in partes:
        if isinstance(p, dict):
            nomes.append(p.get("nome", ""))
            poloPassivo = p.get("pessoa", {})
            if isinstance(poloPassivo, dict):
                nomes.append(poloPassivo.get("nome", ""))
        elif isinstance(p, str):
            nomes.append(p)
    return " ".join(nomes).lower()


def _texto_assuntos(assuntos):
    if not assuntos:
        return ""
    nomes = []
    for a in assuntos:
        if isinstance(a, dict):
            nomes.append(a.get("nome", ""))
        elif isinstance(a, str):
            nomes.append(a)
    return " ".join(nomes).lower()


def mapear_jurisprudencia(assuntos, partes):
    """
    Identifica a categoria de jurisprudência mais adequada com base
    nos assuntos do processo e nos nomes das partes.
    """
    texto = (_texto_assuntos(assuntos) + " " + _texto_partes(partes)).lower()

    melhor_chave = "generico"
    melhor_score = 0

    for chave, bloco in JURISPRUDENCIA_JEC.items():
        if chave == "generico":
            continue
        score = sum(1 for g in bloco["gatilhos"] if g in texto)
        if score > melhor_score:
            melhor_score = score
            melhor_chave = chave

    bloco = dict(JURISPRUDENCIA_JEC[melhor_chave])
    bloco["categoria"] = melhor_chave
    return bloco
