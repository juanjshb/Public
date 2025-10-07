# 🚀 Sistema de Automatización de Usuarios Active Directory

Este sistema automatiza la creación de usuarios en Active Directory cuando el departamento de RRHH registra nuevos empleados en su sistema.

## 📋 Descripción

El proyecto monitorea una base de datos SQL Server en busca de nuevos empleados registrados y automáticamente:
- Crea usuarios en Active Directory
- Genera nombres de usuario únicos
- Asigna contraseñas temporales
- Configura correos electrónicos
- Maneja colisiones de nombres de usuario

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **Base de Datos (SQL Server)**
   - Tabla `PendingADUsers`: Almacena empleados pendientes de procesar
   - Trigger `trg_NewEmployee_AD`: Detecta nuevos empleados automáticamente

2. **Script de Automatización (Python)**
   - `run.py`: Procesa usuarios pendientes y los crea en AD

3. **Active Directory**
   - Crea/actualiza usuarios en la OU especificada

## 📁 Estructura de Archivos

```
proyecto-ad/
├── requirements.txt      # Dependencias de Python
├── run.py               # Script principal de automatización
├── 1_tables.sql         # Creación de tabla de usuarios pendientes
├── 2_triggers.sql       # Trigger para detección automática
├── .env                 # Configuración de entorno (NO SUBIR A GIT)
└── README.md           # Esta documentación
```

## ⚙️ Configuración

### 1. Variables de Entorno (.env)

Crear archivo `.env` con la siguiente configuración:

```env
DB_CONN=DRIVER={SQL Server};SERVER=MI_SERVIDOR;DATABASE=SPN;Trusted_Connection=yes;
AD_BASE_DN=OU=Usuarios,DC=empresa,DC=com
AD_DEFAULT_PASSWORD=CambioTemporal123*
EMAIL_DOMAIN=empresa.com.do
```

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración de Base de Datos

Ejecutar en orden:
```sql
-- 1. Crear tabla de usuarios pendientes
EXEC 1_tables.sql

-- 2. Crear trigger de detección automática
EXEC 2_triggers.sql
```

## 🔄 Flujo de Trabajo

### Proceso Automático
1. **RRHH registra empleado** en tabla `Empleados`
2. **Trigger detecta** nuevo registro y lo inserta en `PendingADUsers`
3. **Script Python** procesa usuarios pendientes:
   - Genera username (ej: `jperez` para Juan Pérez)
   - Crea usuario en Active Directory
   - Asigna contraseña temporal
   - Configura email automáticamente
   - Marca como procesado en la BD

### Manejo de Colisiones
- Si usuario existe y está **inactivo**: Se reactiva
- Si usuario existe y está **activo**: Crea variante con inicial del segundo nombre
- Si variante también existe: Agrega número secuencial

## 🎯 Uso

### Ejecución Manual
```bash
python run.py
```

### Ejecución Programada (Recomendado)
Configurar en Task Scheduler de Windows para ejecutar periódicamente:

```bash
# Ejemplo ejecución cada 30 minutos
python C:\ruta\al\proyecto\run.py
```

## 📊 Estructura de la Base de Datos

### Tabla: PendingADUsers
| Campo | Tipo | Descripción |
|-------|------|-------------|
| Id | INT | Identificador único |
| EmpID | INT | ID del empleado en sistema RRHH |
| Nombre | NVARCHAR(100) | Nombre del empleado |
| Apellido | NVARCHAR(100) | Apellido del empleado |
| Email | NVARCHAR(150) | Correo electrónico |
| Username | NVARCHAR(100) | Nombre de usuario en AD |
| Procesado | BIT | Indicador de procesamiento (0=Pendiente, 1=Procesado) |
| FechaRegistro | DATETIME | Fecha de registro automático |

## 🔒 Seguridad

- Las contraseñas se gestionan mediante variables de entorno
- Conexión trusted a SQL Server
- Usuarios se crean inicialmente deshabilitados (se activan automáticamente)

## 🐛 Solución de Problemas

### Errores Comunes

1. **Error de conexión a BD**
   - Verificar `DB_CONN` en `.env`
   - Confirmar que el servicio SQL Server esté ejecutándose

2. **Error de permisos AD**
   - Ejecutar con cuenta con permisos de creación de usuarios
   - Verificar `AD_BASE_DN` existe

3. **Usuarios duplicados**
   - El sistema maneja automáticamente colisiones
   - Revisar logs para ver variantes creadas

### Logs de Ejecución
El script muestra en consola:
- ✅ Usuarios creados exitosamente
- 🔄 Usuarios reactivados
- ⚠️ Usuarios con variantes
- ❌ Errores de procesamiento

## 📝 Notas Importantes

- **NO SUBIR el archivo `.env`** al control de versiones
- Verificar permisos de ejecución en el dominio
- Las contraseñas temporales deben cumplir políticas de dominio
- Realizar pruebas en ambiente de desarrollo primero
- Ajuster el trigger segun la base de datos de Capital Humano

## 🤝 Soporte

Para reportar problemas o solicitar mejoras, contactar al equipo de sistemas.
