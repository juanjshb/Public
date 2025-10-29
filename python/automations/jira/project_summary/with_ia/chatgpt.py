import os
from datetime import datetime
import pandas as pd
from jira import JIRA
import requests
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------
# 1️⃣ CONFIGURACIÓN
# ---------------------------
load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROYECTO = "PROY"

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_TOKEN))
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------
# 2️⃣ EXTRAER DATOS DE JIRA
# ---------------------------
query = f'project = {PROYECTO} AND updated >= -7d ORDER BY updated DESC'
issues = jira.search_issues(query, maxResults=False)

data = []
for i in issues:
    data.append({
        "Clave": i.key,
        "Resumen": i.fields.summary,
        "Estado": i.fields.status.name,
        "Asignado": i.fields.assignee.displayName if i.fields.assignee else None,
        "Descripción": i.fields.description if i.fields.description else "",
    })

# Generar dataframe y texto base para el prompt
df = pd.DataFrame(data)
texto_issues = "\n".join([
    f"{row.Clave} - {row.Resumen} | Estado: {row.Estado} | Asignado: {row.Asignado}"
    for row in df.itertuples()
])

# ---------------------------
# 3️⃣ GENERAR RESUMEN CON IA
# ---------------------------
prompt = f"""
Eres un asistente de gestión de proyectos. Con base en los siguientes issues de Jira del proyecto {PROYECTO}, 
genera un informe semanal profesional con el siguiente formato:

1. Resumen ejecutivo (máximo 3 oraciones).
2. Avances de la semana anterior (lista breve de tareas completadas).
3. Próximos pasos (qué se planea hacer la próxima semana).
4. Problemas y riesgos (bloqueos, riesgos, acciones sugeridas).
5. Información adicional (salud del proyecto, presupuesto, cronograma).

Datos de los issues de esta semana:
{texto_issues}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",  # o "gpt-4-turbo" si quieres más capacidad
    messages=[{"role": "system", "content": "Eres un gestor de proyectos experto."},
              {"role": "user", "content": prompt}],
    temperature=0.6
)

resumen_ia = response.choices[0].message.content

# ---------------------------
# 4️⃣ ENVIAR A SLACK
# ---------------------------
payload = {"text": f"*📅 Informe del proyecto {PROYECTO} – Semana {datetime.now().strftime('%d/%m/%Y')}*\n\n{resumen_ia}"}
response = requests.post(SLACK_WEBHOOK_URL, json=payload)

if response.status_code == 200:
    print("✅ Informe generado con IA y enviado correctamente a Slack.")
else:
    print(f"❌ Error al enviar el mensaje: {response.status_code} – {response.text}")
