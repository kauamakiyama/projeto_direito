"""
Base de jurisprudência consolidada para análise jurimétrica.
Cobre os tipos de causa mais comuns no JEC.
"""

JURISPRUDENCIA_JEC = {
    "cobranca_indevida": {
        "gatilhos": ["cobrança indevida", "débito indevido", "negativação indevida",
                     "protesto indevido", "banco", "cartão", "financeira",
                     "inscrição indevida", "spc", "serasa"],
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
        "gatilhos": ["não entrega", "atraso entrega", "produto não recebido",
                     "extravio", "e-commerce", "compra online", "loja virtual",
                     "mercadoria"],
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
        "gatilhos": ["plano de saúde", "convênio médico", "negativa cobertura",
                     "recusa procedimento", "operadora saúde", "ans", "saúde suplementar"],
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
        "gatilhos": ["fraude", "cartão clonado", "saque indevido", "golpe",
                     "phishing", "transferência não autorizada", "pix indevido",
                     "clonagem"],
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
        "gatilhos": ["telefonia", "internet", "cancelamento", "rescisão",
                     "multa fidelidade", "serviço não prestado",
                     "claro", "vivo", "tim", "oi", "net", "anatel"],
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
        "gatilhos": ["produto com defeito", "vício oculto", "garantia",
                     "produto defeituoso", "mal funcionamento",
                     "produto parou de funcionar", "vício do produto"],
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
    """Extrai um texto unificado dos nomes das partes."""
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
