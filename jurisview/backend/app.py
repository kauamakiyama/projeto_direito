"""
Decisômetro — backend Flask.
Roda em http://localhost:5000.
"""

import os
import json
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from anthropic import Anthropic

import datajud
import jurisprudencia
import prompts
import monitor

load_dotenv()

app = Flask(__name__)
CORS(app)

monitor.init_db()
_scheduler = monitor.iniciar_scheduler()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(
    api_key=ANTHROPIC_API_KEY,
    timeout=120.0,
    max_retries=2,
) if ANTHROPIC_API_KEY else None

MODELO_CLAUDE = "claude-sonnet-4-5"


def _formatar_valor(v):
    if v is None:
        return "Não informado"
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(v)


def _formatar_data(s):
    dt = datajud._parse_data(s)
    if dt:
        return dt.strftime("%d/%m/%Y")
    return str(s) if s else ""


def _extrair_json(texto: str):
    """Extrai JSON da resposta do Claude, mesmo se vier com cercas markdown."""
    texto = texto.strip()
    # remove cercas ```json ... ```
    if texto.startswith("```"):
        texto = re.sub(r"^```(?:json)?\s*", "", texto)
        texto = re.sub(r"\s*```$", "", texto)
    # tenta achar o primeiro { até o último }
    inicio = texto.find("{")
    fim = texto.rfind("}")
    if inicio != -1 and fim != -1:
        texto = texto[inicio:fim + 1]
    return json.loads(texto)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/analisar", methods=["POST"])
def analisar():
    body = request.get_json(silent=True) or {}
    numero = (body.get("numero_processo") or "").strip()

    if not numero:
        return jsonify({"erro": "Informe o número do processo."}), 400

    # 1) Consulta DataJud
    try:
        processo = datajud.buscar_processo(numero)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": f"Falha ao consultar a base do CNJ: {e}"}), 503

    if not processo:
        return jsonify({
            "erro": "Processo não encontrado na base do CNJ. "
                    "Verifique o número ou se o processo está em segredo de justiça."
        }), 404

    # 2) Extrai dados base
    assuntos = processo.get("assuntos", [])
    partes = processo.get("partes") or processo.get("poloPassivo") or []
    movimentos = processo.get("movimentos", [])
    grau = processo.get("grau")
    data_ajuizamento = processo.get("dataAjuizamento")

    # 3) Jurisprudência + tempo + status
    juris = jurisprudencia.mapear_jurisprudencia(assuntos, partes)
    tempo = datajud.calcular_tempo(data_ajuizamento)
    status = datajud.detectar_status_recurso(movimentos, grau)
    movimentos_fmt = datajud.formatar_movimentos(movimentos)

    # 4) Prompt para o Claude
    dados_para_prompt = {
        **processo,
        "movimentos": movimentos_fmt,
        "status_recurso": status,
    }
    prompt_texto = prompts.montar_prompt(dados_para_prompt, juris, tempo)

    if not client:
        return jsonify({
            "erro": "ANTHROPIC_API_KEY não configurada no backend (.env)."
        }), 503

    # 5) Chamada ao Claude
    try:
        resposta = client.messages.create(
            model=MODELO_CLAUDE,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt_texto}],
        )
        conteudo = resposta.content[0].text
        analise = _extrair_json(conteudo)
    except json.JSONDecodeError as e:
        return jsonify({"erro": f"Resposta da IA fora do formato esperado: {e}"}), 503
    except Exception as e:
        return jsonify({"erro": f"Falha na análise da IA: {type(e).__name__}: {e}"}), 503

    # 6) Monta resposta final com dados brutos + análise
    classe = processo.get("classe", {})
    classe_nome = classe.get("nome") if isinstance(classe, dict) else str(classe)

    orgao = processo.get("orgaoJulgador", {})
    orgao_nome = orgao.get("nome") if isinstance(orgao, dict) else str(orgao)

    resultado = {
        "processo": {
            "numero_processo": datajud.formatar_numero_cnj(processo.get("numeroProcesso", numero)),
            "tribunal": processo.get("tribunal") or processo.get("_tribunal_alias", "").upper(),
            "classe": classe_nome,
            "assuntos": [a.get("nome") if isinstance(a, dict) else a for a in assuntos],
            "valor_causa": _formatar_valor(processo.get("valorCausa")),
            "data_ajuizamento": _formatar_data(data_ajuizamento),
            "orgao_julgador": orgao_nome,
            "grau": grau,
        },
        "analise": analise,
        "movimentos_brutos": movimentos_fmt,
        "fonte": "DataJud CNJ + jurisprudência consolidada",
    }
    return jsonify(resultado)


@app.route("/api/monitorar", methods=["POST"])
def monitorar():
    body = request.get_json(silent=True) or {}
    numero    = (body.get("numero_processo") or "").strip()
    email     = (body.get("email") or "").strip()
    movimentos = body.get("movimentos", [])

    if not numero or not email:
        return jsonify({"erro": "Número do processo e email são obrigatórios."}), 400

    import re as _re
    if not _re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"erro": "Email inválido."}), 400

    ok = monitor.adicionar_inscricao(numero, email, movimentos)
    if ok:
        return jsonify({
            "sucesso": True,
            "mensagem": f"Alertas ativados! Você será notificado em {email} quando houver novas movimentações.",
        })
    return jsonify({"erro": "Erro interno ao ativar alertas."}), 500


@app.route("/cancelar")
def cancelar_notificacao():
    numero = request.args.get("processo", "").strip()
    email  = request.args.get("email", "").strip()
    if not numero or not email:
        return "Link inválido.", 400
    monitor.remover_inscricao(numero, email)
    return f"""<html><head><meta charset="utf-8">
    <style>body{{font-family:-apple-system,sans-serif;text-align:center;padding:60px;color:#1e293b}}</style>
    </head><body>
      <h2>Alertas cancelados</h2>
      <p>Você não receberá mais notificações do processo <strong>{numero}</strong>.</p>
      <a href="/">Voltar ao início</a>
    </body></html>"""


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
