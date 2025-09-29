from pydantic import BaseModel, Field, condecimal
from typing import Literal

class Transaccion(BaseModel):
    cliente_id: str = Field(..., description="Identificador interno del cliente (se anonimiza)")
    monto: condecimal(gt=0)  # monto > 0
    hora: int = Field(..., ge=0, le=23)
    pais: Literal["DO", "US", "VE", "HT"]  # limitar a países válidos
