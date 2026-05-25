"""
Módulo de comunicação com a API pública do DataJud (CNJ).

A API DataJud é gratuita e a chave abaixo é pública (consta na documentação
oficial do CNJ). Os dados têm defasagem de horas/dias e processos em segredo
de justiça não aparecem.
"""

import requests
from datetime import datetime, timezone

# Chave pública oficial do CNJ — pode ser comitada
DATAJUD_API_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
BASE_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
TIMEOUT = 10

# Mapeamento J (segmento) + TR (código tribunal) -> alias do endpoint
TRIBUNAIS_ESTADUAIS = {
    "26": "tjsp",
    "19": "tjrj",
    "13": "tjmg",
    "07": "tjce",
    "06": "tjpa",
    "05": "tjba",
    "16": "tjma",
    "21": "tjpe",
    "24": "tjrs",
    "16": "tjma",
    "08": "tjdft",
    "09": "tjes",
    "10": "tjgo",
    "11": "tjmt",
    "12": "tjms",
    "14": "tjpb",
    "15": "tjpr",
    "17": "tjpi",
    "18": "tjrn",
    "20": "tjro",
    "22": "tjrr",
    "23": "tjsc",
    "25": "tjse",
    "27": "tjto",
    "01": "tjac",
    "02": "tjal",
    "03": "tjap",
    "04": "tjam",
}


def extrair_tribunal(numero_processo: str) -> str:
    """
    Extrai a sigla do alias DataJud a partir do número CNJ.
    Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
    """
    limpo = numero_processo.replace("-", ".").replace(" ", "")
    partes = limpo.split(".")
    if len(partes) < 5:
        raise ValueError("Número de processo inválido (formato CNJ esperado).")

    # partes: [NNNNNNN, DD, AAAA, J, TR, OOOO]
    segmento = partes[3]
    tr = partes[4].zfill(2)

    if segmento == "8":  # Justiça Estadual
        return TRIBUNAIS_ESTADUAIS.get(tr, "tjsp")
    if segmento == "5":  # Justiça Federal
        return f"trf{int(tr)}"
    if segmento == "4":  # Justiça do Trabalho
        if tr == "90":
            return "tst"
        return f"trt{int(tr)}"
    if segmento == "7":  # Justiça Militar Estadual
        return "stm"
    # Fallback
    return "tjsp"


def buscar_processo(numero_processo: str):
    """
    Consulta o processo no DataJud. Retorna _source ou None.
    """
    tribunal = extrair_tribunal(numero_processo)
    url = BASE_URL.format(tribunal=tribunal)

    numero_limpo = numero_processo.replace("-", "").replace(".", "").replace(" ", "")

    payload = {
        "query": {
            "match": {
                "numeroProcesso": numero_limpo
            }
        }
    }

    headers = {
        "Authorization": DATAJUD_API_KEY,
        "Content-Type": "application/json",
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    hits = data.get("hits", {}).get("hits", [])
    if not hits:
        return None

    fonte = hits[0].get("_source", {})
    fonte["_tribunal_alias"] = tribunal
    return fonte


def formatar_movimentos(movimentos):
    """Ordena movimentos do mais recente para o mais antigo e formata."""
    if not movimentos:
        return []

    def parse_data(m):
        try:
            return datetime.fromisoformat(m.get("dataHora", "").replace("Z", "+00:00"))
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)

    ordenados = sorted(movimentos, key=parse_data, reverse=True)
    resultado = []
    for m in ordenados:
        dt = parse_data(m)
        data_fmt = dt.strftime("%d/%m/%Y") if dt != datetime.min.replace(tzinfo=timezone.utc) else ""
        resultado.append({
            "codigo": m.get("codigo"),
            "nome": m.get("nome", ""),
            "dataHora": data_fmt,
            "complementos": m.get("complementosTabelados", []),
        })
    return resultado


def detectar_status_recurso(movimentos, grau):
    """Analisa movimentações para determinar status processual."""
    codigos = {m.get("codigo") for m in (movimentos or [])}

    em_recurso = (grau == "G2")

    if 848 in codigos:
        return {
            "status": "transitado_julgado",
            "descricao": "Processo transitou em julgado — decisão final.",
            "em_recurso": False,
        }
    if 54 in codigos and em_recurso:
        return {
            "status": "recurso_julgado",
            "descricao": "Recurso já foi julgado pela Turma Recursal (acórdão proferido).",
            "em_recurso": True,
        }
    if em_recurso:
        return {
            "status": "em_recurso",
            "descricao": "Processo está em fase de recurso na Turma Recursal.",
            "em_recurso": True,
        }
    if 12223 in codigos:
        return {
            "status": "sentenciado",
            "descricao": "Sentença já foi proferida em 1ª instância.",
            "em_recurso": False,
        }
    if 26 in codigos:
        return {
            "status": "concluso",
            "descricao": "Processo está concluso ao juiz para decisão.",
            "em_recurso": False,
        }
    return {
        "status": "em_andamento",
        "descricao": "Processo em andamento normal.",
        "em_recurso": False,
    }


def calcular_tempo(data_ajuizamento: str):
    """Calcula dias e meses decorridos desde o ajuizamento."""
    if not data_ajuizamento:
        return {"dias_decorridos": 0, "meses_decorridos": 0, "data_formatada": ""}

    try:
        dt = datetime.fromisoformat(data_ajuizamento.replace("Z", "+00:00"))
    except Exception:
        return {"dias_decorridos": 0, "meses_decorridos": 0, "data_formatada": ""}

    agora = datetime.now(timezone.utc)
    dias = (agora - dt).days
    meses = round(dias / 30)
    return {
        "dias_decorridos": dias,
        "meses_decorridos": meses,
        "data_formatada": dt.strftime("%d/%m/%Y"),
    }
