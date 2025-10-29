# 🤖 Jira Weekly Reporter – con IA (ChatGPT / Gemini)

Este proyecto automatiza la generación y envío de reportes semanales de estado de proyectos Jira, utilizando inteligencia artificial (IA) para redactar resúmenes ejecutivos profesionales.

Incluye dos implementaciones:
- **`chatgpt.py`** → usa la API de OpenAI (ChatGPT).
- **`gemini.py`** → usa la API de Google Gemini.

Los informes se generan automáticamente y se envían al canal de Slack del equipo.

---

## 🚀 Características

✅ Extrae issues actualizados de un proyecto en **Jira**.  
✅ Resume y clasifica la información (completadas, en progreso, bloqueadas).  
✅ Genera un **informe ejecutivo redactado con IA** (ChatGPT o Gemini).  
✅ Envía automáticamente el resumen al canal de **Slack**.  
✅ Soporte para formato Markdown compatible con Slack.  
✅ Estructura de informe:
- **Resumen ejecutivo**
- **Avances de la semana anterior**
- **Próximos pasos**
- **Problemas y riesgos**
- **Información adicional** (salud, presupuesto, cronograma)

---

## 🧩 Requisitos previos

- Python 3.9 o superior  
- Acceso a:
  - Una instancia de **Jira Cloud** con API habilitada
  - Un **Webhook de Slack** para notificaciones
  - API Key de **OpenAI** y/o **Google Gemini**

---

## ⚙️ Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/jira-ai-reporter.git
   cd jira-ai-reporter
    ````

2. Crea un entorno virtual y actívalo:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea un archivo `.env` con tus credenciales:

   ```env
   # --- Jira ---
   JIRA_SERVER=https://tuempresa.atlassian.net
   JIRA_USER=tu_usuario@empresa.com
   JIRA_TOKEN=tu_token_api
   JIRA_PROJECT=PROY

   # --- Slack ---
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/XXXX/XXXX

   # --- ChatGPT ---
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx

   # --- Gemini ---
   GEMINI_API_KEY=AIzaSyXXXXXX
   ```

---

## 🧠 Uso

### 🟢 Opción 1: Usar ChatGPT

Genera el reporte usando el modelo GPT de OpenAI.

```bash
python report_chatgpt.py
```

### 🔵 Opción 2: Usar Gemini

Genera el reporte usando el modelo Gemini de Google.

```bash
python report_gemini.py
```

Ambos scripts:

* Consultan los issues actualizados de la última semana.
* Generan un resumen con IA.
* Envían el reporte al canal configurado en Slack.

---

## 📤 Ejemplo de salida en Slack

```
📅 Informe del proyecto PROY – Semana que termina el 29/10/2025

Resumen ejecutivo:
El proyecto avanza según lo planificado, con varias tareas clave completadas.

✅ Avances de la semana anterior:
- PROY-23: Implementación de login
- PROY-45: Ajuste de UI en reportes

🚀 Próximos pasos:
- Integrar API de clientes externos
- Revisar documentación técnica

⚠️ Problemas y riesgos:
- Retraso en validación de QA (PROY-61)

📊 Información adicional:
- Salud del proyecto: 🟢 En buen camino
- Presupuesto: Dentro de lo estimado
- Cronograma: Cumpliendo fechas previstas
```

---

## 🕐 Automatización

Puedes programar la ejecución semanal del script (por ejemplo, los viernes) usando:

### Linux / macOS – `cron`

```bash
crontab -e
# Ejecutar cada viernes a las 9 AM
0 9 * * FRI /ruta/a/tu/venv/bin/python /ruta/al/script/report_chatgpt.py
```

### Windows – Task Scheduler

Crea una tarea programada que ejecute:

```
python "C:\ruta\al\script\report_gemini.py"
```

---

## 📦 Dependencias principales

```txt
jira
pandas
requests
python-dotenv
openai
google-generativeai
```

---

## 🔒 Seguridad

* No compartas tus tokens ni los subas al repositorio.
* Agrega el archivo `.env` a tu `.gitignore`.
* Usa roles limitados para los tokens de Jira y Slack.

---

## 🧭 Próximas mejoras

* [ ] Soporte para múltiples proyectos Jira.
* [ ] Enviar reportes en formato HTML o PDF.
* [ ] Análisis de métricas (velocidad, bloqueos, cumplimiento).
* [ ] Detección automática de “riesgos emergentes”.
* [ ] Panel web para visualización histórica.

---

## 👨‍💻 Autor

**Tu Nombre / Equipo**

> Automatización + IA aplicada a gestión de proyectos.
> [LinkedIn](https://linkedin.com/in/tuusuario) · [GitHub](https://github.com/tuusuario)

---

## 📜 Licencia

MIT License – libre para usar, modificar y mejorar.

```

---

¿Quieres que te genere también el **`requirements.txt`** correspondiente (con versiones estables y compatibles para ambos scripts)?  
Así puedes dejar el proyecto totalmente listo para ejecutar o desplegar en un servidor.
```
