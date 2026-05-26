"""
Monitoramento de processos: inscrições, detecção de mudanças e notificações por email.
"""

import hashlib
import logging
import os
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

log = logging.getLogger(__name__)

DB_PATH = os.getenv("MONITOR_DB", os.path.join(os.path.dirname(__file__), "monitor.db"))


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inscricoes (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_processo   TEXT NOT NULL,
            email             TEXT NOT NULL,
            ultimo_hash       TEXT,
            ultima_verificacao TEXT,
            ativo             INTEGER DEFAULT 1,
            criado_em         TEXT DEFAULT (datetime('now')),
            UNIQUE(numero_processo, email)
        )
    """)
    conn.commit()
    conn.close()


def _hash_movimentos(movimentos: list) -> str:
    chaves = sorted(
        f"{m.get('codigo', '')}-{m.get('dataHora', '')}-{m.get('nome', '')}"
        for m in movimentos
    )
    return hashlib.md5("\n".join(chaves).encode()).hexdigest()


def adicionar_inscricao(numero_processo: str, email: str, movimentos_atuais: list) -> bool:
    hash_atual = _hash_movimentos(movimentos_atuais)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """INSERT INTO inscricoes (numero_processo, email, ultimo_hash, ultima_verificacao)
               VALUES (?, ?, ?, datetime('now'))
               ON CONFLICT(numero_processo, email) DO UPDATE SET
                 ativo = 1,
                 ultimo_hash = excluded.ultimo_hash,
                 ultima_verificacao = excluded.ultima_verificacao""",
            (numero_processo, email, hash_atual),
        )
        conn.commit()
        return True
    except Exception as e:
        log.error("Erro ao adicionar inscrição: %s", e)
        return False
    finally:
        conn.close()


def remover_inscricao(numero_processo: str, email: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE inscricoes SET ativo = 0 WHERE numero_processo = ? AND email = ?",
        (numero_processo, email),
    )
    conn.commit()
    conn.close()


def _enviar_email(email: str, numero_processo: str, movimentos: list) -> bool:
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")
    app_url   = os.getenv("APP_URL", "http://localhost:5000")

    if not smtp_host or not smtp_user or not smtp_pass:
        log.warning("SMTP não configurado — notificação ignorada para %s", email)
        return False

    linhas = "".join(
        f'<li style="margin-bottom:8px"><strong>{m.get("dataHora","")}</strong>'
        f' — {m.get("nome","") or m.get("codigo","")}</li>'
        for m in movimentos[:5]
    )
    cancelar_url = f"{app_url}/cancelar?processo={numero_processo}&email={email}"

    html_body = f"""
    <div style="font-family:-apple-system,sans-serif;max-width:600px;margin:0 auto;color:#1e293b">
      <div style="background:#0D2137;padding:24px 32px;border-radius:10px 10px 0 0">
        <h1 style="margin:0;color:white;font-size:20px">Nova movimentação detectada</h1>
        <p style="margin:6px 0 0;color:rgba(255,255,255,.65);font-size:13px">{numero_processo}</p>
      </div>
      <div style="background:#f8fafc;padding:28px 32px;border-radius:0 0 10px 10px;
                  border:1px solid #e2e8f0;border-top:none">
        <p style="margin:0 0 16px">
          Detectamos <strong>novas movimentações</strong> no processo que você está monitorando:
        </p>
        <ul style="padding-left:20px;margin:0 0 24px">{linhas}</ul>
        <a href="{app_url}"
           style="background:#0D2137;color:white;padding:12px 22px;border-radius:7px;
                  text-decoration:none;font-size:14px;font-weight:600">
          Ver análise completa
        </a>
        <hr style="margin:28px 0;border:none;border-top:1px solid #e2e8f0">
        <p style="margin:0;font-size:12px;color:#94a3b8">
          Para cancelar as notificações deste processo,
          <a href="{cancelar_url}" style="color:#64748b">clique aqui</a>.
        </p>
      </div>
    </div>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Nova movimentação — {numero_processo}"
    msg["From"]    = f"JurisView <{smtp_user}>"
    msg["To"]      = email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(smtp_user, smtp_pass)
            srv.sendmail(smtp_user, [email], msg.as_string())
        log.info("Email enviado para %s (processo %s)", email, numero_processo)
        return True
    except Exception as e:
        log.error("Falha ao enviar email para %s: %s", email, e)
        return False


def verificar_atualizacoes():
    """Chamado pelo scheduler a cada 6h: verifica mudanças e notifica."""
    import datajud  # importação local para evitar ciclo

    conn = sqlite3.connect(DB_PATH)
    inscricoes = conn.execute(
        "SELECT id, numero_processo, email, ultimo_hash FROM inscricoes WHERE ativo = 1"
    ).fetchall()
    conn.close()

    log.info("Verificando %d inscrição(ões)...", len(inscricoes))

    for sub_id, numero, email, hash_anterior in inscricoes:
        try:
            dados = datajud.buscar_processo(numero)
            if not dados:
                continue

            movimentos = datajud.formatar_movimentos(dados.get("movimentos", []))
            hash_atual = _hash_movimentos(movimentos)

            if hash_atual == hash_anterior:
                continue

            _enviar_email(email, numero, movimentos)

            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                "UPDATE inscricoes SET ultimo_hash = ?, ultima_verificacao = datetime('now') WHERE id = ?",
                (hash_atual, sub_id),
            )
            conn.commit()
            conn.close()
            log.info("Atualização detectada e notificada: processo %s → %s", numero, email)

        except Exception as e:
            log.error("Erro ao verificar processo %s: %s", numero, e)


def iniciar_scheduler():
    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        verificar_atualizacoes,
        "interval",
        hours=6,
        id="monitor_processos",
        misfire_grace_time=300,
    )
    scheduler.start()
    log.info("Scheduler de monitoramento iniciado (intervalo: 6h)")
    return scheduler
