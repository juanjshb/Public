import os
from datetime import datetime
from jira import JIRA
from dotenv import load_dotenv
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# ==============================================================
# 1️⃣ CONFIGURACIÓN Y AUTENTICACIÓN
# ==============================================================

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO", "").split(",")

if not all([JIRA_SERVER, JIRA_USER, JIRA_TOKEN, EMAIL_FROM, EMAIL_PASS]):
    raise EnvironmentError("⚠️ Faltan variables de entorno obligatorias.")

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_TOKEN))


# ==============================================================
# 2️⃣ FUNCIONES AUXILIARES
# ==============================================================

def obtener_issues_por_version(version_nombre, proyecto="PROD"):
    query = f'project = {proyecto} AND fixVersion = "{version_nombre}" ORDER BY priority DESC'
    issues = jira.search_issues(query, maxResults=False)
    data = []
    for issue in issues:
        data.append({
            "Clave": issue.key,
            "Resumen": issue.fields.summary or "",
            "Descripción": issue.fields.description or "",
            "Estado": issue.fields.status.name,
            "Reporter": issue.fields.reporter.displayName if issue.fields.reporter else "",
            "URL": f"{JIRA_SERVER}/browse/{issue.key}",
            "Version": version_nombre
        })
    return pd.DataFrame(data)


def generar_release_html(df, version):
    if df.empty:
        return f"<h3>No hay tickets asociados a la versión {version}</h3>"

    html = f"""
    <html>
    <body style="font-family:Arial, sans-serif;">
        <h2>🚀 Version {version}</h2>
        <h3>What's New 🤔</h3>
    """
    for _, row in df.iterrows():
        descripcion = (row["Descripción"] or "").replace("\n", "<br>")
        html += f"""
        <div style="margin-bottom:20px; border-bottom:1px solid #ccc; padding-bottom:10px;">
            <h3>{row['Resumen']}</h3>
            <p><b>🗝 Jira:</b> <a href="{row['URL']}">{row['Clave']}</a> | <b>Estado:</b> {row['Estado']}</p>
            <p>{descripcion}</p>
        </div>
      """
        
    html += f"<p style='font-size:12px;color:gray;'>Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"
    html += "</body></html>"
    return html


def enviar_email(destinatarios, asunto, html_body, adjunto=None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = asunto
    msg.attach(MIMEText(html_body, "html"))

    if adjunto and os.path.exists(adjunto):
        with open(adjunto, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(adjunto))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(adjunto)}"'
            msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)
        print(f"✅ Release Notes enviadas a {', '.join(destinatarios)}")


# ==============================================================
# 3️⃣ PROCESO PRINCIPAL
# ==============================================================

VERSION_ACTUAL = os.getenv("RELEASE_VERSION", "2.46")
PROYECTO = os.getenv("JIRA_PROJECT", "PROD")

df = obtener_issues_por_version(VERSION_ACTUAL, PROYECTO)
html = generar_release_html(df, VERSION_ACTUAL)

# Guardar también como HTML local
file_name = f"release_notes_{VERSION_ACTUAL.replace('.', '_')}.html"
with open(file_name, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Release Notes generadas para la versión {VERSION_ACTUAL}")
enviar_email(EMAIL_TO, f"🚀 Release Notes - Version {VERSION_ACTUAL}", html)
