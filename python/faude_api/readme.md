#    	🛡️ API de Detección de Fraude Bancario (República Dominicana)

Este proyecto es una API REST en Python (FastAPI) que detecta
transacciones bancarias sospechosas de fraude utilizando Machine
Learning (Isolation Forest).
El diseño sigue las normativas dominicanas de:

-   Ley Monetaria y Financiera No. 183-02
-   Ley 155-17 Contra el Lavado de Activos y Financiamiento del
    Terrorismo
-   Ley 172-13 de Protección de Datos Personales
-   Circulares de la Superintendencia de Bancos (SIB) sobre
    ciberseguridad y monitoreo de operaciones.

  ⚠️ Aviso: Este proyecto es una demostración técnica. Los datos son
  simulados.
  Para producción se requieren análisis legales, cifrado de datos reales
  y procedimientos adicionales.

------------------------------------------------------------------------

##    🚀 Características

-   Detección de anomalías con IsolationForest.
-   Anonimización de identificadores de clientes usando SHA-256 (cumple
    Ley 172-13).
-   Registro de alertas en un archivo JSON para auditoría
    (trazabilidad).
-   API REST con FastAPI para integración con sistemas bancarios o
    aplicaciones web.

------------------------------------------------------------------------

##    📂 Estructura del proyecto

    fraude_api/
    │
    ├─ main.py               # API principal (FastAPI)
    ├─ models.py             # Esquema de datos (Pydantic)
    ├─ detector.py           # Lógica de ML y auditoría
    └─ auditoria/
       └─ alertas.json       # Log de alertas (almacenado de forma segura)

------------------------------------------------------------------------

##    ⚙️ Requisitos

-   Python 3.9 o superior
-   Paquetes:
    -   fastapi
    -   uvicorn
    -   pandas
    -   scikit-learn

Instalar dependencias:

    pip install fastapi uvicorn pandas scikit-learn

------------------------------------------------------------------------

##    ▶️ Ejecución

1.  Clonar este repositorio:

        git clone https://github.com/tu_usuario/fraude_api.git
        cd fraude_api

2.  Iniciar el servidor:

        uvicorn main:app --reload

3.  Probar la API:

    -   Endpoint principal: POST http://127.0.0.1:8000/analizar
    -   Documentación interactiva (Swagger): http://127.0.0.1:8000/docs

------------------------------------------------------------------------

##    📤 Ejemplo de solicitud

POST /analizar

    {
      "cliente_id": "12345",
      "monto": 12500,
      "hora": 3,
      "pais": "DO"
    }

Respuesta:

    {
      "fraude_sospechoso": true,
      "score_riesgo": -0.12,
      "cliente_hash": "f8a2...e45c",
      "pais": "DO",
      "timestamp": "2025-09-29T17:45:31.123Z"
    }

------------------------------------------------------------------------

##    🏛️ Cumplimiento legal

  ---------------------------------------------------------------------------
  Aspecto          Implementación            Relación con la ley
  ---------------- ------------------------- --------------------------------
  Protección de    Hash irreversible del     Minimiza riesgo de
  datos (Ley       cliente_id                reidentificación.
  172-13)                                    

  Trazabilidad     auditoria/alertas.json    Evidencia para auditoría y
  (SIB)            con timestamp, score y    reportes.
                   motivo                    

  Finalidad        Procesamiento exclusivo   Compatible con Ley 183-02 y
  legítima         para detección de fraude  155-17.

  Consentimiento   Debe implementarse en     Requisito en producción.
                   contratos/UX              
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

##    🔒 Recomendaciones para producción

-   Base de datos cifrada (PostgreSQL/MSSQL) en lugar de JSON plano.
-   TLS/HTTPS obligatorio para todas las comunicaciones.
-   Logs firmados digitalmente (PGP o SFTP seguro).
-   Reentrenamiento periódico para evitar concept drift.
-   Monitoreo humano antes de bloquear cuentas.

------------------------------------------------------------------------

##    📜 Licencia

Este proyecto se distribuye bajo la licencia MIT.
No se garantiza cumplimiento legal en entornos productivos sin las
configuraciones adicionales requeridas por las autoridades dominicanas.

------------------------------------------------------------------------

##    👤 Autor

-  Desarrollado por Juan Jesús Herrera Benítez
-  Rol: Systems Manager & ICT Project Leader

------------------------------------------------------------------------

##    ⚠️ Aviso

-  Aunque mencionado al principio recordar que esto es un ejemplo para demostrar la posibilidad de utilizar API e IA para la deteccion de fraude. El ejemplo debe ser actualizado y aplicar politicas internas de la institucion bancaria.



