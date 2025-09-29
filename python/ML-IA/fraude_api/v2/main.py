# [file name]: main.py
# [file content begin]
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import detector
from models import Transaccion, TransaccionResponse, HealthCheck, TasasCambio
import logging
import asyncio

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Detección de Fraude Bancario Multi-Moneda",
    description="Sistema de detección de transacciones fraudulentas con soporte para DOP, USD y EUR",
    version="3.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    logger.info("🚀 API de Detección de Fraude Multi-Moneda iniciada")
    logger.info("📊 Cargando modelo ML y tasas de cambio...")
    # Precargar tasas de cambio al iniciar
    detector.obtener_tasas_cambio()

@app.on_event("shutdown")
async def shutdown_event():
    """Evento al cerrar la aplicación"""
    logger.info("🛑 Cerrando API de Detección de Fraude")
    detector.cerrar_modelo()

@app.post("/analizar", response_model=TransaccionResponse, summary="Analizar transacción para fraude")
async def analizar_transaccion(transaccion: Transaccion):
    """
    Analiza una transacción bancaria para detectar posibles patrones fraudulentos.
    Soporta múltiples monedas (DOP, USD, EUR) con conversión automática a DOP.
    
    Args:
        transaccion: Datos de la transacción a analizar
    
    Returns:
        TransaccionResponse: Resultado detallado del análisis con conversión de moneda
    """
    try:
        logger.info(f"Analizando transacción: {transaccion.monto} {transaccion.moneda} para cliente: {transaccion.cliente_id[:8]}...")
        
        # Usar el detector mejorado con soporte multi-moneda
        resultado = detector.detectar_fraude(
            cliente_id=transaccion.cliente_id,
            monto=float(transaccion.monto),
            moneda=transaccion.moneda,
            hora=transaccion.hora,
            pais=transaccion.pais
        )
        
        # Preparar respuesta estructurada
        respuesta = TransaccionResponse(
            fraude_detectado=resultado["es_fraude"],
            probabilidad_fraude=resultado["probabilidad_fraude"],
            nivel_riesgo=resultado["analisis_riesgo"]["nivel_riesgo"],
            factores_riesgo=resultado["analisis_riesgo"]["factores_riesgo"],
            mensaje=resultado["mensaje"],
            recomendacion=resultado["recomendacion"],
            cliente_hash=resultado["cliente_hash"],
            score_anomalia=resultado["score_anomalia"],
            timestamp=resultado["timestamp"],
            datos_analizados=resultado["datos_recibidos"],
            conversion_moneda=resultado["conversion_moneda"]
        )
        
        nivel_riesgo = resultado["analisis_riesgo"]["nivel_riesgo"]
        monto_dop = resultado["monto_dop"]
        logger.info(f"✅ Análisis completado. Fraude: {resultado['es_fraude']}, Riesgo: {nivel_riesgo}, Monto DOP: {monto_dop}")
        
        return respuesta
        
    except Exception as e:
        logger.error(f"❌ Error analizando transacción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/tasas-cambio", summary="Obtener tasas de cambio actuales")
async def obtener_tasas():
    """
    Obtiene las tasas de cambio actuales desde el BHD
    """
    try:
        tasas_info = detector.obtener_estado_tasas()
        return {
            "status": "success",
            "tasas": tasas_info["tasas_actuales"],
            "actualizado": tasas_info["cache_actualizado"],
            "fuente": "BHD Leon API"
        }
    except Exception as e:
        logger.error(f"❌ Error obteniendo tasas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo tasas de cambio: {str(e)}")

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Endpoint de salud del servicio con estado de tasas"""
    tasas_info = detector.obtener_estado_tasas()
    return {
        "status": "healthy", 
        "timestamp": detector.datetime.utcnow().isoformat(),
        "service": "fraud-detection-api-multi-currency",
        "version": "3.0.0",
        "tasas_cambio": {
            "estado": tasas_info["estado"],
            "actualizado": tasas_info["cache_actualizado"]
        }
    }

@app.get("/")
async def root():
    return {
        "mensaje": "API de Detección de Fraude Bancario Multi-Moneda - República Dominicana",
        "version": "3.0.0",
        "estado": "Operativo",
        "monedas_soportadas": ["DOP", "USD", "EUR"],
        "documentacion": "/docs",
        "endpoints": {
            "analizar": "POST /analizar",
            "tasas_cambio": "GET /tasas-cambio", 
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }
# [file content end]