import os
from datetime import datetime
import pandas as pd
from jira import JIRA
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# ==============================================================
# 1️⃣ CONFIGURACIÓN Y AUTENTICACIÓN
# ==============================================================

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROYECTO = os.getenv("JIRA_PROJECT", "PROY")

# Validaciones básicas
missing = [k for k, v in {
    "JIRA_SERVER": JIRA_SERVER,
    "JIRA_USER": JIRA_USER,
    "JIRA_TOKEN": JIRA_TOKEN,
    "SLACK_WEBHOOK_URL": SLACK_WEBHOOK_URL,
    "GEMINI_API_KEY": GEMINI_API_KEY
}.items() if not v]

if missing:
    raise EnvironmentError(f"⚠️ Faltan variables de entorno: {', '.join(missing)}")

# Configurar conexión a Jira
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_TOKEN))

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================
# 2️⃣ OBTENER DATOS DE JIRA
# ==============================================================

query = f'project = {PROYECTO} AND updated >= -7d ORDER BY updated DESC'
issues = jira.search_issues(query, maxResults=False)

if not issues:
    print("ℹ️ No se encontraron issues actualizados en los últimos 7 días.")
    exit(0)

data = []
for i in issues:
    data.append({
        "Clave": i.key,
        "Resumen": i.fields.summary or "",
        "Estado": i.fields.status.name or "",
        "Asignado": i.fields.assignee.displayName if i.fields.assignee else "Sin asignar",
        "Descripción": i.fields.description or "",
    })

# Crear DataFrame (opcional, por si se quiere guardar)
df = pd.DataFrame(data)

# Texto simplificado para el prompt de la IA
texto_issues = "\n".join([
    f"{row.Clave} - {row.Resumen} | Estado: {row.Estado} | Asignado: {row.Asignado}"
    for row in df.itertuples()
])

# ==============================================================
# 3️⃣ GENERAR RESUMEN EJECUTIVO CON IA (Gemini)
# ==============================================================

prompt = f"""
Eres un asistente experto en gestión de proyectos.
Con base en los siguientes issues del proyecto *{PROYECTO}*, genera un informe ejecutivo semanal claro y conciso.

Formato esperado:
1. **Resumen ejecutivo:** máximo 3 oraciones con el estado general del proyecto.
2. **Avances de la semana anterior:** lista breve de tareas completadas.
3. **Próximos pasos:** tareas o prioridades para la próxima semana.
4. **Problemas y riesgos:** bloqueos, riesgos y acciones sugeridas.
5. **Información adicional:** salud general del proyecto (🟢🟡🔴), presupuesto y cronograma.

Datos de los issues:
{texto_issues}
"""

try:
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    resumen_ia = response.text.strip()
except Exception as e:
    print(f"❌ Error al generar resumen con Gemini: {e}")
    resumen_ia = "⚠️ No se pudo generar el resumen automático."

# ==============================================================
# 4️⃣ ENVIAR INFORME A SLACK
# ==============================================================

fecha = datetime.now().strftime("%d/%m/%Y")

slack_message = {
    "text": (
        f"*📅 Informe del proyecto {PROYECTO} – Semana que termina el {fecha}*\n\n"
        f"{resumen_ia}"
    )
}

try:
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)
    response.raise_for_status()
    print("✅ Informe generado con IA y enviado correctamente a Slack.")
except requests.RequestException as e:
    print(f"❌ Error al enviar mensaje a Slack: {e}")
