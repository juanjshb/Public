# [file name]: models.py
# [file content begin]
from pydantic import BaseModel, Field, condecimal, validator
from typing import Literal, Optional
from decimal import Decimal
import re

class Transaccion(BaseModel):
    cliente_id: str = Field(..., 
        description="Identificador interno del cliente (se anonimiza)",
        min_length=1,
        max_length=50,
        example="CL-123456789")
    
    monto: condecimal(gt=0, decimal_places=2) = Field(...,
        description="Monto de la transacción (debe ser mayor a 0)",
        example=12500.50)
    
    moneda: Literal["DOP", "USD", "EUR"] = Field(...,
        description="Moneda de la transacción",
        example="DOP")
    
    hora: int = Field(..., 
        ge=0, 
        le=23,
        description="Hora de la transacción (0-23)",
        example=14)
    
    pais: Literal["DO", "US", "VE", "HT", "PR", "MX", "CO", "ES", "FR", "DE"] = Field(...,
        description="País de origen de la transacción",
        example="DO")
    
    @validator('cliente_id')
    def validate_cliente_id(cls, v):
        if not re.match(r'^[A-Za-z0-9\-_]+$', v):
            raise ValueError('El ID de cliente contiene caracteres inválidos')
        return v
    
    @validator('monto')
    def validate_monto(cls, v):
        monto_float = float(v)
        if monto_float > 1000000:
            raise ValueError('El monto excede el límite permitido')
        return v

class TransaccionResponse(BaseModel):
    fraude_detectado: bool
    probabilidad_fraude: float
    nivel_riesgo: str
    factores_riesgo: list
    mensaje: str
    recomendacion: str
    cliente_hash: str
    score_anomalia: float
    timestamp: str
    datos_analizados: dict
    conversion_moneda: Optional[dict] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: str
    tasas_cambio: Optional[dict] = None

class TasasCambio(BaseModel):
    USD_compra: float
    USD_venta: float
    EUR_compra: float
    EUR_venta: float
    actualizado: str
# [file content end]