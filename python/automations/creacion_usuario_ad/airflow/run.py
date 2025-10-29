##airflow variables set DB_CONN "DRIVER={SQL Server};SERVER=TU_SERVIDOR;DATABASE=SPN;Trusted_Connection=yes;"
##airflow variables set AD_BASE_DN "OU=Usuarios,DC=empresa,DC=com"
##airflow variables set AD_DEFAULT_PASSWORD "CambioTemporal123*"
##airflow variables set EMAIL_DOMAIN "dominio.com.do"

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pyodbc
import re
from pyad import aduser, adcontainer, adquery

# --- Configuración Airflow Variables ---
DB_CONN = Variable.get("DB_CONN")  # Ej: DRIVER={SQL Server};SERVER=SERVIDOR;DATABASE=SPN;Trusted_Connection=yes;
AD_BASE_DN = Variable.get("AD_BASE_DN")  # Ej: "OU=Usuarios,DC=empresa,DC=com"
AD_DEFAULT_PASSWORD = Variable.get("AD_DEFAULT_PASSWORD", default_var="CambioTemporal123*")
EMAIL_DOMAIN = Variable.get("EMAIL_DOMAIN", default_var="dominio.com.do")

# --- Funciones auxiliares ---
def normalizar(texto):
    """Limpia y pone en formato simple."""
    if not texto:
        return ""
    return re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s-]", "", texto.strip()).title()

def generar_username(nombre, segundo_nombre, apellido):
    base = (nombre[0] + apellido).lower()
    return re.sub(r"\s+", "", base)

def usuario_existe(username):
    q = adquery.ADQuery()
    q.execute_query(
        attributes=["distinguishedName", "sAMAccountName", "userAccountControl"],
        where_clause=f"sAMAccountName = '{username}'",
        base_dn=AD_BASE_DN,
    )
    results = list(q.get_results())
    return results[0] if results else None

def esta_activo(user_dn):
    user = aduser.ADUser.from_dn(user_dn)
    return not user.is_account_disabled()

def crear_o_actualizar_usuario(nombre, segundo_nombre, apellido, email):
    username = generar_username(nombre, segundo_nombre, apellido)
    ou = adcontainer.ADContainer.from_dn(AD_BASE_DN)
    full_name = f"{nombre} {apellido}"

    # --- Si email está vacío, se genera automáticamente ---
    if not email or email.strip() == "":
        email = f"{username}@{EMAIL_DOMAIN}"
        print(f"Email vacío detectado. Se asigna automáticamente: {email}")

    # --- Verificar si el usuario ya existe ---
    user_info = usuario_existe(username)

    if not user_info:
        print(f"Creando usuario: {username}")
        user = aduser.ADUser.create(username, ou, password=AD_DEFAULT_PASSWORD)
        user.update_attribute("displayName", full_name)
        user.update_attribute("givenName", nombre)
        user.update_attribute("sn", apellido)
        user.update_attribute("mail", email)
        user.enable()
        return username

    user_dn = user_info["distinguishedName"]
    user = aduser.ADUser.from_dn(user_dn)

    if not esta_activo(user_dn):
        print(f"Usuario {username} existe pero está deshabilitado. Reactivando...")
        user.enable()
        user.update_attribute("displayName", full_name)
        user.update_attribute("givenName", nombre)
        user.update_attribute("sn", apellido)
        user.update_attribute("mail", email)
        return username
    else:
        # Usuario activo: buscar variación con segundo nombre
        if segundo_nombre:
            username_alt = (nombre[0] + segundo_nombre[0] + apellido).lower()
            user_alt_info = usuario_existe(username_alt)
            if not user_alt_info:
                print(f"Usuario {username} activo, creando variante {username_alt}")
                user = aduser.ADUser.create(username_alt, ou, password=AD_DEFAULT_PASSWORD)
                user.update_attribute("displayName", f"{nombre} {segundo_nombre} {apellido}")
                user.update_attribute("givenName", f"{nombre} {segundo_nombre}")
                user.update_attribute("sn", apellido)
                user.update_attribute("mail", email)
                user.enable()
                return username_alt
            else:
                counter = 1
                while usuario_existe(f"{username_alt}{counter}"):
                    counter += 1
                final_username = f"{username_alt}{counter}"
                print(f"⚙️ Creando usuario alternativo: {final_username}")
                user = aduser.ADUser.create(final_username, ou, password=AD_DEFAULT_PASSWORD)
                user.update_attribute("displayName", full_name)
                user.update_attribute("givenName", nombre)
                user.update_attribute("sn", apellido)
                user.update_attribute("mail", email)
                user.enable()
                return final_username

def get_pending_users():
    conn = pyodbc.connect(DB_CONN)
    cursor = conn.cursor()
    cursor.execute("SELECT Id, Nombre, SegundoNombre, Apellido, Email FROM dbo.PendingADUsers WHERE Procesado = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_processed(user_id, username):
    conn = pyodbc.connect(DB_CONN)
    cursor = conn.cursor()
    cursor.execute("UPDATE dbo.PendingADUsers SET Procesado = 1, Username = ? WHERE Id = ?", username, user_id)
    conn.commit()
    conn.close()

def process_users(**context):
    usuarios = get_pending_users()
    for u in usuarios:
        user_id, nombre, segundo_nombre, apellido, email = u
        nombre, segundo_nombre, apellido, email = map(normalizar, (nombre, segundo_nombre, apellido, email))
        try:
            username_final = crear_o_actualizar_usuario(nombre, segundo_nombre, apellido, email)
            mark_processed(user_id, username_final)
        except Exception as e:
            print(f"❌ Error con {nombre} {apellido}: {e}")

# --- Definición del DAG ---
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['admin@dominio.com.do'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'sync_ad_users_dag',
    default_args=default_args,
    description='Sincroniza usuarios pendientes desde SQL Server a Active Directory',
    schedule_interval='@hourly',  # cada hora
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['active_directory', 'sync']
) as dag:

    sync_users_task = PythonOperator(
        task_id='sync_ad_users',
        python_callable=process_users,
        provide_context=True,
    )

    sync_users_task
