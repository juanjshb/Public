import os
from datetime import datetime, timedelta
from jira import JIRA
from dotenv import load_dotenv
import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import google.generativeai as genai

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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not all([JIRA_SERVER, JIRA_USER, JIRA_TOKEN, EMAIL_FROM, EMAIL_PASS, GEMINI_API_KEY]):
    raise EnvironmentError("⚠️ Faltan variables de entorno obligatorias.")

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_TOKEN))
genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================
# 2️⃣ FUNCIONES AUXILIARES
# ==============================================================

def extraer_texto_desde_jira(value):
    """Convierte el campo de descripción (ADF o string) a texto plano."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and "content" in value:
        text = ""
        for item in value.get("content", []):
            text += extraer_texto_desde_jira(item)
        return text
    if isinstance(value, list):
        return "".join(extraer_texto_desde_jira(v) for v in value)
    if "text" in value:
        return value.get("text", "")
    return str(value)


def obtener_todos_los_tickets(proyecto="PROD", dias=7):
    """Obtiene los tickets del proyecto de los últimos N días."""
    fecha_inicio = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
    query = f'project = {proyecto} AND updated >= "{fecha_inicio}" ORDER BY updated DESC'
    url = f"{JIRA_SERVER}/rest/api/3/search/jql"

    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_TOKEN)
    params = {
        "jql": query,
        "maxResults": 1000,
        "fields": "summary,description,status,reporter,assignee,issuetype,created,updated"
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    response.raise_for_status()

    issues_data = response.json().get("issues", [])
    data = []

    for issue in issues_data:
        fields = issue.get("fields", {})
        data.append({
            "Clave": issue.get("key", ""),
            "Resumen": fields.get("summary", ""),
            "Descripción": extraer_texto_desde_jira(fields.get("description")),
            "Tipo": fields.get("issuetype", {}).get("name", ""),
            "Estado": fields.get("status", {}).get("name", ""),
            "Asignado a": (fields.get("assignee") or {}).get("displayName", "No asignado"),
            "Reportado por": fields.get("reporter", {}).get("displayName", ""),
            "Creado": fields.get("created", ""),
            "Actualizado": fields.get("updated", ""),
            "URL": f"{JIRA_SERVER}/browse/{issue.get('key', '')}"
        })
        
    return pd.DataFrame(data)


def generar_resumen_gemini(df, proyecto):
    """Usa Gemini IA para generar un resumen ejecutivo."""
    if df.empty:
        return f"No hubo actividad registrada en los últimos 14 días para el proyecto {proyecto}."

    tickets_texto = "\n".join([
        f"- [{r['Clave']}] {r['Resumen']} (Estado: {r['Estado']}, Tipo: {r['Tipo']})"
        for _, r in df.iterrows()
    ])

    prompt = f"""
Eres un Project Manager experto. A partir de la siguiente lista de tickets del proyecto {proyecto}, 
redacta un **resumen ejecutivo** en tono profesional. 
Debes identificar claramente:

1️⃣ Qué se logró o cerró recientemente (estado 'Done', 'Closed', 'Resolved', etc.).
2️⃣ Qué se encuentra en curso o en pruebas ('In Progress', 'Testing', etc.).
3️⃣ Qué está pendiente de iniciar o bloqueado ('To Do', 'Blocked', etc.).
4️⃣ Incluye una breve visión general de la evolución del proyecto y próximos pasos.

Lista de tickets:
{tickets_texto}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


def generar_html_proyecto(df, proyecto, resumen):
    """Genera un informe HTML con resumen ejecutivo."""
    if df.empty:
        return f"<h3>No hay tickets registrados en el proyecto {proyecto}</h3>"

    html = f"""
    <html>
    <body style="font-family:Arial, sans-serif;">
        <h2>📊 Resumen Ejecutivo – Proyecto {proyecto}</h2>
        <p>{resumen}</p>
        <hr>
        <h3>📋 Detalle de Tickets (últimos 14 días)</h3>
        <p>Total de tickets: <b>{len(df)}</b></p>
        <hr>
    """

    for _, row in df.iterrows():
        descripcion = (row["Descripción"] or "").replace("\n", "<br>")
        html += f"""
        <div style="margin-bottom:15px; border-bottom:1px solid #ddd; padding-bottom:10px;">
            <h3>{row['Resumen']}</h3>
            <p>
                <b>🗝 Clave:</b> <a href="{row['URL']}">{row['Clave']}</a> |
                <b>Tipo:</b> {row['Tipo']} |
                <b>Estado:</b> {row['Estado']}<br>
                <b>👤 Asignado a:</b> {row['Asignado a']} |
                <b>📅 Creado:</b> {row['Creado'][:10]} |
                <b>🔄 Actualizado:</b> {row['Actualizado'][:10]}
            </p>
            <p>{descripcion}</p>
        </div>
        """

    html += f"<p style='font-size:12px;color:gray;'>Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"
    html += "</body></html>"
    return html


def enviar_email(destinatarios, asunto, html_body, adjunto=None):
    """Envía un correo con el HTML y opcionalmente un adjunto."""
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

    with smtplib.SMTP_SSL("mail.inpartnergroup.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)
        print(f"✅ Informe enviado a {', '.join(destinatarios)}")


# ==============================================================
# 3️⃣ PROCESO PRINCIPAL (Versión con depuración)
# ==============================================================
try:
    print("Iniciando script...")
    
    # Comprobar la autenticación de JIRA primero
    print(f"Paso 1: Autenticando en JIRA ({JIRA_SERVER})...")
    # jira = JIRA(...) ya se hizo arriba, podemos probar la conexión
    user = jira.myself()
    print(f"Paso 2: Autenticación exitosa como '{user['displayName']}'")

    PROYECTO = os.getenv("JIRA_PROJECT", "PROD")
    print(f"Paso 3: Obteniendo tickets para el proyecto '{PROYECTO}'...")
    
    df = obtener_todos_los_tickets(PROYECTO)
    
    print(f"Paso 4: Se obtuvieron {len(df)} tickets.")
    print("Paso 5: Generando resumen con Gemini IA...")

    resumen_gemini = generar_resumen_gemini(df, PROYECTO)
    
    print("Paso 6: Resumen de Gemini recibido.")
    print("Paso 7: Generando informe HTML...")

    html = generar_html_proyecto(df, PROYECTO, resumen_gemini)

    file_name = f"tickets_{PROYECTO}_{datetime.now().strftime('%Y%m%d')}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html)

    print("==============================================================")
    print(f"✅ Informe generado para el proyecto {PROYECTO} ({len(df)} tickets)")
    print(f"📄 Archivo: {file_name}")
    print("🧠 Resumen Ejecutivo (Gemini):")
    print(resumen_gemini)
    print("==============================================================")

    # Si quieres enviarlo por correo, descomenta:
    # print("Paso 8: Enviando correo...")
    # enviar_email(EMAIL_TO, f"📊 Resumen Ejecutivo – {PROYECTO}", html, file_name)
    # print("Paso 9: Correo enviado.")

except Exception as e:
    print(f"❌ ERROR: El script falló.")
    print(e)
