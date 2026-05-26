"""
Módulo de comunicação com a API pública do DataJud (CNJ).

A API DataJud é gratuita e a chave abaixo é pública (consta na documentação
oficial do CNJ). Os dados têm defasagem de horas/dias e processos em segredo
de justiça não aparecem.
"""

import re
import requests
from datetime import datetime, timezone

# Chave pública oficial do CNJ — pode ser comitada
DATAJUD_API_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
BASE_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
TIMEOUT = 10


def _parse_data(s) -> datetime | None:
    """
    Parseia datas do DataJud em múltiplos formatos:
      - ISO:            2024-01-15T10:30:00  /  2024-01-15T10:30:00Z
      - YYYYMMDDHHMMSS: 20240115103000
      - YYYYMMDD:       20240115
    """
    if not s:
        return None
    s = str(s).strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        pass
    digits = re.sub(r"\D", "", s)
    if len(digits) >= 8:
        try:
            year, month, day = int(digits[0:4]), int(digits[4:6]), int(digits[6:8])
            if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                return datetime(year, month, day, tzinfo=timezone.utc)
        except ValueError:
            pass
    return None

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
    Consulta o processo no DataJud.
    Busca até 5 hits para encontrar tanto o G1 quanto o G2.
    Para processos em recurso (G2), usa a data de ajuizamento do G1,
    que é a data real do início da ação — o G2 registra apenas a
    entrada do recurso no tribunal, não o ajuizamento original.
    """
    tribunal = extrair_tribunal(numero_processo)
    url = BASE_URL.format(tribunal=tribunal)
    numero_limpo = numero_processo.replace("-", "").replace(".", "").replace(" ", "")

    payload = {
        "query": {"match": {"numeroProcesso": numero_limpo}},
        "size": 5,
    }
    headers = {
        "Authorization": DATAJUD_API_KEY,
        "Content-Type": "application/json",
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    hits = resp.json().get("hits", {}).get("hits", [])
    if not hits:
        return None

    # Separa hits por grau
    g1, g2 = None, None
    for hit in hits:
        src = hit.get("_source", {})
        grau = src.get("grau", "")
        if grau == "G1" and g1 is None:
            g1 = src
        elif grau == "G2" and g2 is None:
            g2 = src

    # Processo em recurso: usa G2 como base mas completa com dados do G1
    if g2 is not None:
        if g1 is not None:
            # Data de ajuizamento: usa G1 se for mais antiga (data real da ação)
            dt_g1 = _parse_data(g1.get("dataAjuizamento"))
            dt_g2 = _parse_data(g2.get("dataAjuizamento"))
            if dt_g1 and (dt_g2 is None or dt_g1 < dt_g2):
                g2["dataAjuizamento"] = g1.get("dataAjuizamento")
            # Valor da causa: G2 geralmente não tem
            if not g2.get("valorCausa"):
                g2["valorCausa"] = g1.get("valorCausa")
            # Partes: G2 geralmente não tem
            if not g2.get("partes"):
                g2["partes"] = g1.get("partes", [])
            # Movimentos: combina G2 (recurso) + G1 (1ª instância) sem duplicatas
            movs_g2 = g2.get("movimentos", [])
            movs_g1 = g1.get("movimentos", [])
            codigos_g2 = {(m.get("codigo"), m.get("dataHora")) for m in movs_g2}
            extras = [m for m in movs_g1 if (m.get("codigo"), m.get("dataHora")) not in codigos_g2]
            g2["movimentos"] = movs_g2 + extras
        g2["_tribunal_alias"] = tribunal
        return g2

    # Processo de 1ª instância
    fonte = g1 or hits[0].get("_source", {})
    fonte["_tribunal_alias"] = tribunal
    return fonte


def formatar_movimentos(movimentos):
    """Ordena movimentos do mais recente para o mais antigo e formata."""
    if not movimentos:
        return []

    _epoch = datetime.min.replace(tzinfo=timezone.utc)

    def parse_data(m):
        return _parse_data(m.get("dataHora")) or _epoch

    ordenados = sorted(movimentos, key=parse_data, reverse=True)
    resultado = []
    for m in ordenados:
        dt = parse_data(m)
        data_fmt = dt.strftime("%d/%m/%Y") if dt != _epoch else ""
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


def formatar_numero_cnj(numero: str) -> str:
    """Converte número raw (20 dígitos) para o formato CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO"""
    d = re.sub(r"\D", "", str(numero))
    if len(d) != 20:
        return numero
    return f"{d[0:7]}-{d[7:9]}.{d[9:13]}.{d[13]}.{d[14:16]}.{d[16:20]}"


def calcular_tempo(data_ajuizamento: str):
    """Calcula dias e meses decorridos desde o ajuizamento."""
    dt = _parse_data(data_ajuizamento)
    if not dt:
        return {"dias_decorridos": 0, "meses_decorridos": 0, "data_formatada": ""}

    agora = datetime.now(timezone.utc)
    dias = (agora - dt).days
    meses = round(dias / 30)
    return {
        "dias_decorridos": dias,
        "meses_decorridos": meses,
        "data_formatada": dt.strftime("%d/%m/%Y"),
    }
