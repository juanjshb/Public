import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
from jira import JIRA
from dotenv import load_dotenv
import google.generativeai as genai
from fpdf import FPDF

# ==============================================================
# 1️⃣ CONFIGURACIÓN Y AUTENTICACIÓN
# ==============================================================

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO", "").split(",")

PROYECTOS = os.getenv("JIRA_PROJECTS", "PROY1,PROY2").split(",")

missing = [k for k, v in {
    "JIRA_SERVER": JIRA_SERVER,
    "JIRA_USER": JIRA_USER,
    "JIRA_TOKEN": JIRA_TOKEN,
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "EMAIL_FROM": EMAIL_FROM,
    "EMAIL_PASS": EMAIL_PASS
}.items() if not v]

if missing:
    raise EnvironmentError(f"⚠️ Faltan variables de entorno: {', '.join(missing)}")

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_TOKEN))
genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================
# 2️⃣ FUNCIONES AUXILIARES
# ==============================================================

def obtener_issues(jira, proyectos, dias=7):
    data = []
    for proyecto in proyectos:
        query = f'project = {proyecto} AND updated >= -{dias}d ORDER BY updated DESC'
        issues = jira.search_issues(query, maxResults=False)
        for i in issues:
            data.append({
                "Proyecto": proyecto,
                "Clave": i.key,
                "Resumen": i.fields.summary or "",
                "Estado": i.fields.status.name or "",
                "Asignado": i.fields.assignee.displayName if i.fields.assignee else "Sin asignar",
                "Descripción": i.fields.description or "",
                "Creado": i.fields.created,
                "Actualizado": i.fields.updated,
            })
    return pd.DataFrame(data)


def analizar_metricas(df):
    metricas = {}
    for proyecto, grupo in df.groupby("Proyecto"):
        completadas = grupo[grupo["Estado"].str.lower().isin(["done", "resuelto", "cerrado"])]
        bloqueadas = grupo[grupo["Estado"].str.lower().str.contains("bloqueado")]
        metricas[proyecto] = {
            "Total": len(grupo),
            "Completadas": len(completadas),
            "Bloqueadas": len(bloqueadas),
            "Velocidad (%)": round(len(completadas) / len(grupo) * 100, 1) if len(grupo) else 0
        }
    return metricas


def detectar_riesgos(df):
    riesgos = []
    for row in df.itertuples():
        texto = (row.Resumen + " " + (row.Descripción or "")).lower()
        if any(word in texto for word in ["bloqueado", "riesgo", "error", "problema", "retraso"]):
            riesgos.append(f"{row.Clave} - {row.Resumen} ({row.Asignado})")
    return riesgos


def generar_reporte_html(resumen, metricas, riesgos):
    html = f"""
    <html><body>
    <h2>📊 Informe Semanal de Proyectos - {datetime.now().strftime('%d/%m/%Y')}</h2>
    <h3>Resumen Ejecutivo</h3>
    <p>{resumen}</p>
    <h3>Métricas</h3>
    <ul>
    """
    for p, m in metricas.items():
        html += f"<li><b>{p}</b> - Total: {m['Total']} | Completadas: {m['Completadas']} | Bloqueadas: {m['Bloqueadas']} | Velocidad: {m['Velocidad (%)']}%</li>"
    html += "</ul>"

    if riesgos:
        html += "<h3>⚠️ Riesgos emergentes</h3><ul>"
        html += "".join(f"<li>{r}</li>" for r in riesgos)
        html += "</ul>"
    else:
        html += "<p>✅ No se detectaron riesgos relevantes esta semana.</p>"

    html += "</body></html>"
    return html


def generar_pdf(html, output_file="informe.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Informe Semanal de Proyectos", align="C")
    pdf.multi_cell(0, 10, txt="(ver versión HTML para formato completo)")
    pdf.output(output_file)
    return output_file


def enviar_email(destinatarios, asunto, html_body, adjunto_pdf):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = asunto

    msg.attach(MIMEText(html_body, "html"))

    with open(adjunto_pdf, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(adjunto_pdf))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(adjunto_pdf)}"'
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)
        print(f"✅ Correo enviado a {', '.join(destinatarios)}")


# ==============================================================
# 3️⃣ PROCESAMIENTO PRINCIPAL
# ==============================================================

df = obtener_issues(jira, PROYECTOS)

texto_issues = "\n".join([
    f"{row.Proyecto} - {row.Clave} - {row.Resumen} | Estado: {row.Estado} | Asignado: {row.Asignado}"
    for row in df.itertuples()
])

prompt = f"""
Eres un analista experto en gestión de proyectos y riesgos, especializado en metodologías ágiles y sistemas Jira.

Tu tarea es generar un informe de estatus **completo y crítico** a partir del siguiente listado de issues de varios proyectos. Analiza el estado, la asignación y la descripción de cada issue para extraer el máximo valor.

---
**DATOS DE ISSUES DE JIRA:**
{texto_issues}
---

**INFORME REQUERIDO:**

Genera un informe estructurado en las siguientes secciones. Sé preciso, conciso y utiliza un tono objetivo y preventivo:

### 1. Resumen Ejecutivo de Estatus (General)
* Proporciona una visión general del progreso (**verde, amarillo o rojo**).
* Menciona los **logros clave** de la semana (issues cerrados, avances significativos).
* Identifica los **proyectos o áreas más activas** y las más estancadas.

### 2. Análisis Crítico y Detección de Errores (Retrospectiva)
* **Problemas de Asignación:** Identifica personas con una carga de trabajo aparentemente excesiva (alto número de issues 'En Progreso') y posibles cuellos de botella.
* **Errores de Flujo:** Señala issues que llevan demasiado tiempo en un estado intermedio ('Abierto', 'Pendiente de Revisión', 'En Test') sin moverse, indicando un posible *stuck flow*. Menciona las claves de estos issues.
* **Desalineación:** Detecta cualquier aparente desalineación entre el 'Resumen' (lo que se hace) y el 'Estado' (dónde está) que pueda indicar un mal uso del tablero de Jira.

### 3. Predicción de Bloqueadores (Stoppers) y Riesgos (Prospectiva)
* **Stoppers Potenciales:** Basado en el estancamiento de issues clave o la sobrecarga de un asignado, predice qué issues específicos (menciona su `Clave`) tienen más probabilidad de convertirse en un bloqueo crítico en la próxima semana.
* **Riesgos de Proyecto:** Identifica riesgos de alto nivel para la planificación general (ej., Riesgo de retraso en el Proyecto X por dependencia no resuelta en la Clave Y).
* **Dependencias Críticas:** Señala cualquier issue que parezca ser una dependencia clave para que otros issues puedan avanzar.

### 4. Recomendaciones de Mejora y Acción (Accionable)
* Ofrece **tres acciones claras y priorizadas** que el equipo de gestión debe tomar inmediatamente (ej., "Reasignar la Clave ABC-123", "Establecer una reunión de aclaración para el Proyecto X", "Mover los issues inactivos a 'Bloqueado'").
* Sugiere **mejoras en el proceso de Jira** (ej., "Fomentar el uso del estado 'Bloqueado'" o "Dividir issues con resúmenes muy amplios").

Asegúrate de que la salida esté bien formateada y sea fácil de leer.
"""

try:
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    resumen_ia = response.text.strip()
except Exception as e:
    resumen_ia = f"⚠️ Error generando resumen con Gemini: {e}"

metricas = analizar_metricas(df)
riesgos = detectar_riesgos(df)
html_reporte = generar_reporte_html(resumen_ia, metricas, riesgos)
pdf_path = generar_pdf(html_reporte)

asunto = f"📅 Informe Semanal de Proyectos ({datetime.now().strftime('%d/%m/%Y')})"
enviar_email(EMAIL_TO, asunto, html_reporte, pdf_path)
