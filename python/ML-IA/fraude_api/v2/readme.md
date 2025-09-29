# 🛡️ API de Detección de Fraude Bancario Multi-Moneda (República Dominicana) v2.0

## 📋 Descripción Mejorada

Sistema avanzado de detección de fraude que combina Machine Learning (Isolation Forest) con reglas de negocio específicas para el contexto bancario dominicano. **Ahora con soporte completo para múltiples monedas (DOP, USD, EUR)** integrado en tiempo real con las tasas de cambio del BHD León.

### 🎯 Nuevas Características Multi-Moneda

- **🔄 Conversión Automática**: Conversión en tiempo real de USD/EUR a DOP usando tasas oficiales
- **📊 API BHD Integrada**: Integración directa con el sistema de tasas del BHD León
- **💾 Cache Inteligente**: Tasas cacheadas por 30 minutos para mejor performance
- **🛡️ Fallback Robusto**: Tasas por defecto si la API no está disponible
- **🌍 Análisis por Divisa**: Nuevos factores de riesgo para transacciones en moneda extranjera

---

## 🚀 Características Principales

### Detección Inteligente Multi-Moneda
- **Modelo ML**: Isolation Forest entrenado con montos en DOP
- **Conversión Automática**: USD/EUR → DOP usando tasas actualizadas
- **Reglas de Negocio**: Factores específicos por tipo de moneda
- **Análisis Combinado**: Decisiones basadas en múltiples criterios monetarios

### Cumplimiento Legal
- **Ley 172-13**: Anonimización con SHA-256 de identificadores
- **Ley 155-17**: Trazabilidad completa para auditoría
- **Circulares SIB**: Monitoreo en tiempo real de operaciones en divisas
- **Normas Monetarias**: Conversión según tasas oficiales bancarias

### Seguridad de Datos
- **Protección de Identidad**: Hash irreversible de clientes
- **Registro Seguro**: Alertas en JSON con detalles de conversión
- **Validación Estricta**: Schemas Pydantic robustos para múltiples monedas

---

## 📊 Respuestas Multi-Moneda

### Ejemplo de Respuesta Mejorada con Conversión

```json
{
  "fraude_detectado": true,
  "probabilidad_fraude": 0.8743,
  "nivel_riesgo": "ALTO",
  "factores_riesgo": [
    "MONTO_ELEVADO",
    "TRANSACCION_DIVISA",
    "DIVISA_MONTO_ELEVADO",
    "HORARIO_NOCTURNO"
  ],
  "mensaje": "ALERTA: Transacción identificada como fraudulenta por modelo ML y reglas de negocio",
  "recomendacion": "Recomendación: Revisar transacción manualmente y contactar al cliente",
  "cliente_hash": "a1b2c3d4e5f67890",
  "score_anomalia": -0.1245,
  "timestamp": "2025-09-29T17:45:31.123Z",
  "conversion_moneda": {
    "monto_original": 1000.0,
    "moneda_original": "USD",
    "monto_dop": 62900.0,
    "tasa_aplicada": 62.9,
    "tipo_tasa": "venta",
    "descripcion": "USD → DOP (tasa venta: 62.9)",
    "conversion_requerida": true
  },
  "datos_analizados": {
    "cliente_id_length": 12,
    "monto_original": 1000.0,
    "moneda_original": "USD",
    "hora_transaccion": 3,
    "pais_origen": "DO"
  }
}
```

### Nuevos Factores de Riesgo Implementados

| Factor | Descripción | Puntaje | Moneda |
|--------|-------------|---------|---------|
| `MONTO_ELEVADO` | Transacciones > $10,000 DOP | +2 | Todas |
| `MONTO_MUY_BAJO` | Transacciones < $50 DOP | +1 | Todas |
| `TRANSACCION_DIVISA` | Operación en USD/EUR | +1 | USD/EUR |
| `DIVISA_MONTO_ELEVADO` | Divisa + monto > $15,000 DOP | +2 | USD/EUR |
| `HORARIO_NOCTURNO` | Entre 12am-6am | +1 | Todas |
| `PAIS_ALTO_RIESGO` | Venezuela, Haití | +2 | Todas |
| `PAIS_RIESGO_MEDIO` | Países no DO/US | +1 | Todas |
| `MONTO_ALTO_HORARIO_SOSPECHOSO` | Combo monto alto + horario nocturno | +2 | Todas |

---

## 🔧 Estructura del Proyecto Mejorada

```
fraude_api/
│
├── main.py                 # API FastAPI con endpoints multi-moneda
├── models.py              # Schemas Pydantic con validación multi-moneda
├── detector.py            # Lógica ML + conversión tasas + reglas negocio
├── auditoria/
│   └── alertas.json       # Log de alertas con detalles de conversión
├── requirements.txt       # Dependencias actualizadas
└── tests/                # Tests unitarios (recomendado)
```

---

## 📚 Endpoints Disponibles

### POST `/analizar`
Analiza transacciones en tiempo real con soporte multi-moneda.

**Body:**
```json
{
  "cliente_id": "CL-123456789",
  "monto": 1000.00,
  "moneda": "USD",
  "hora": 14,
  "pais": "DO"
}
```

**Monedas Soportadas:** `DOP`, `USD`, `EUR`

**Respuestas:**
- `200 OK`: Análisis completado con resultados detallados y conversión
- `422 Validation Error`: Datos de entrada inválidos
- `500 Internal Error`: Error en el servidor

### GET `/tasas-cambio`
Obtiene las tasas de cambio actuales desde el BHD León.

**Respuesta:**
```json
{
  "status": "success",
  "tasas": {
    "USD_compra": 60.9,
    "USD_venta": 62.9,
    "EUR_compra": 71.4,
    "EUR_venta": 76.4,
    "actualizado": "2025-09-29T17:45:31.123Z"
  },
  "actualizado": "2025-09-29T17:30:00.000Z",
  "fuente": "BHD Leon API"
}
```

### GET `/health`
Verifica el estado del servicio incluyendo estado de tasas de cambio.

### GET `/`
Información general de la API y endpoints disponibles.

---

## 🛡️ Cumplimiento Legal Mejorado

| Aspecto Legal | Implementación | Beneficio |
|---------------|----------------|-----------|
| **Protección de Datos** | Hash SHA-256 + validación estricta | Cumple Ley 172-13 |
| **Trazabilidad** | Registro completo con conversiones | Auditoría SIB |
| **Finalidad Legítima** | Exclusivo para prevención de fraude | Ley 183-02 |
| **Tasas Oficiales** | Integración BHD León | Normativa monetaria |
| **Transparencia** | Detalles de conversión en respuestas | Mejores prácticas |

---

## 🔌 Integración con BHD León

### Fuente de Tasas
- **URL**: `https://backend.bhd.com.do/api/modal-cambio-rate?populate=deep`
- **Frecuencia**: Actualización cada 30 minutos
- **Fallback**: Tasas por defecto si API no disponible
- **Monedas**: USD (Compra/Venta), EUR (Compra/Venta)

### Ejemplo de Respuesta BHD
```json
{
  "exchangeRates": [
    {
      "id": 1,
      "heading": "Dólares US$",
      "currency": "USD",
      "buyingRate": 60.9,
      "sellingRate": 62.9
    },
    {
      "id": 2, 
      "heading": "Euros EU€",
      "currency": "EUR",
      "buyingRate": 71.4,
      "sellingRate": 76.4
    }
  ]
}
```

---

## 🚀 Instalación y Uso

```bash
# Clonar repositorio
git clone https://github.com/tu_usuario/fraude_api.git
cd fraude_api

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O usando el script mejorado
python run_server.py
```

**Acceder a la documentación:** http://localhost:8000/docs

---

## 💰 Ejemplos de Conversión

### Transacción en USD
```bash
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "CL-123456789",
    "monto": 1000.00,
    "moneda": "USD", 
    "hora": 14,
    "pais": "DO"
  }'
```

### Transacción en EUR
```bash
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "CL-987654321",
    "monto": 500.00,
    "moneda": "EUR",
    "hora": 3, 
    "pais": "ES"
  }'
```

### Consultar Tasas
```bash
curl "http://localhost:8000/tasas-cambio"
```

---

## 🔒 Recomendaciones para Producción

### Seguridad
- [ ] Implementar TLS/HTTPS obligatorio
- [ ] Base de datos cifrada (PostgreSQL)
- [ ] Autenticación JWT para API
- [ ] Rate limiting por cliente/IP
- [ ] Validación adicional de montos en divisas

### Monitoreo
- [ ] Dashboard de métricas en tiempo real
- [ ] Alertas para fallos en API de tasas
- [ ] Reentrenamiento automático del modelo
- [ ] Auditoría periódica de conversiones

### Escalabilidad
- [ ] Contenedores Docker
- [ ] Load balancer
- [ ] Cache Redis para tasas
- [ ] Base de datos clusterizada
- [ ] Múltiples fuentes de tasas de cambio

---

## 📞 Soporte y Mantenimiento

**Autor:** Juan Jesús Herrera Benítez  
**Experiencia:** Sistemas Bancarios y Cumplimiento Legal  

---

## ⚠️ Aviso Legal Mejorado

Este sistema es una demostración técnica avanzada con soporte multi-moneda. Para implementación en producción:

1. **Validación Legal**: Consultar con departamento legal institucional
2. **Certificación**: Obtener certificaciones requeridas por la SIB
3. **Acuerdos con Bancos**: Establecer acuerdos formales para uso de APIs de tasas
4. **Personalización**: Adaptar a políticas internas específicas de divisas
5. **Pruebas**: Testing exhaustivo con datos reales anonimizados
6. **Backup de Tasas**: Múltiples fuentes de tasas para redundancia

**Versión:** 2.0.0  
**Última actualización:** Septiembre 2025  
**Soporte Multi-Moneda:** ✅ Completo (DOP, USD, EUR)

---

## 🔄 Changelog v2.0 

- ✅ **Soporte completo para USD y EUR**
- ✅ **Integración en tiempo real con API BHD León**
- ✅ **Sistema de cache inteligente (30 minutos)**
- ✅ **Nuevos factores de riesgo para divisas**
- ✅ **Endpoint dedicado para consulta de tasas**
- ✅ **Trazabilidad completa de conversiones**
- ✅ **Manejo robusto de fallos en API de tasas**
- ✅ **Documentación ampliada con ejemplos multi-moneda**

---

**🚀 ¿Listo para detectar fraude en múltiples monedas? ¡Inicia el servidor y comienza a analizar!**


