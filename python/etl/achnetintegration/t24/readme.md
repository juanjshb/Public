# Airflow DAG - Generación de Archivo ACH

Este proyecto implementa un **DAG en Apache Airflow** que extrae las transacciones autorizadas desde **Temenos T24**, las transforma según un **mapeo configurable en base de datos (ACH_MAPPING)** y genera un archivo plano en formato ACH para enviar a la cámara de compensación.

Cabe destacar que esto solo es para mostrar la posibilidad de generar de manera automatizada los archivos otras validaciones pueden ser realizadas, solo procesar transacciones aprobadas y como en la version final agregar los cortes del procesador ademas de una Manager (Interfaz de Usuario) para que como en la version final solo el administrador o manejador de la entidad financiera parametrize los campos.

---

## 📌 Flujo del Proceso

1. Se conecta a la base de datos de T24 usando una conexión de Airflow (`t24_db`).
2. Extrae transacciones autorizadas del día con datos como:
   - Banco origen
   - Banco destino
   - Cuenta origen
   - Cuenta destino
   - Monto
   - Beneficiario
   - Comentario de la transacción
3. Aplica las reglas de posicionamiento definidas en la tabla `ACH_MAPPING`.
4. Genera un archivo plano con nombre `ach_YYYYMMDD.txt` en el directorio configurado en la variable de Airflow `ACH_OUTPUT_DIR`.

---

## ⚙️ Configuración en Airflow

### 1. Variables de Airflow
Configura en **Admin → Variables**:

- `ACH_OUTPUT_DIR`: Ruta donde se generarán los archivos ACH (ej. `/opt/airflow/output/ach`).
- `ACH_ORIGIN_BANK_CODE`: Código ACH del banco emisor (ej. `123456`).

### 2. Conexiones de Airflow
Configura en **Admin → Connections**:

- **Conn Id**: `t24_db`  
- **Conn Type**: Oracle  
- **Host**: `<host de tu BD>`  
- **Schema**: `<schema>`  
- **Login**: `<usuario>`  
- **Password**: `<contraseña>`  
- **Port**: `1521`  

---

## 🗄️ Tablas de Soporte

### Tabla `ACH_MAPPING`

Define el formato de salida (campos, posiciones y longitudes).

```sql
CREATE TABLE ACH_MAPPING (
    FIELD_NAME  VARCHAR2(50) PRIMARY KEY,
    START_POS   NUMBER(5) NOT NULL,
    LENGTH      NUMBER(5) NOT NULL
);

### Ejemplo de `ACH_MAPPING`
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('ORIGIN_BANK_CODE', 1,   6);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('DEST_BANK_CODE',   7,   6);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('TRANSACTION_ID',  13,  15);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('SOURCE_ACCOUNT',  28,  20);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('DEST_ACCOUNT',    48,  20);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('AMOUNT',          68,  12);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('VALUE_DATE',      80,   8);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('BENEF_NAME',      88,  40);
INSERT INTO ACH_MAPPING (FIELD_NAME, START_POS, LENGTH) VALUES ('COMMENT',        128,  60);
COMMIT;
```


### Tabla `ACH_BANKS`

Define los bancos destino (id en T24, codigo en la red ACH).

```sql
CREATE TABLE ACH_BANKS (
    T24_BANK_ID  VARCHAR2(20) PRIMARY KEY,
    ACH_CODE     VARCHAR2(10) NOT NULL
);

INSERT INTO ACH_BANKS (T24_BANK_ID, ACH_CODE) VALUES ('B001', '987654');
INSERT INTO ACH_BANKS (T24_BANK_ID, ACH_CODE) VALUES ('B002', '654321');
COMMIT;
```


## 📂 Estructura del Proyecto

dags/
 └── generate_ach_file.py   # Código del DAG principal
README.md                   # Documentación


**##▶️ Ejecución**

1. Copia generate_ach_file.py en el directorio dags/ de Airflow.
2. Asegúrate de haber configurado las variables y conexiones en Airflow.
3. El DAG se ejecuta automáticamente según la programación definida (@daily por defecto).
4. El archivo resultante se encontrará en el directorio configurado en ACH_OUTPUT_DIR.


**##📑 Notas**

El campo `ORIGIN_BANK_CODE` se carga desde la variable de Airflow `ACH_ORIGIN_BANK_CODE`.
El campo `COMMENT` se alimenta desde `FT.PAYMENT_DETAILS` (o `FT.NARRATIVE` según la parametrización de T24).
El archivo se genera con codificación UTF-8 y formato texto plano.
