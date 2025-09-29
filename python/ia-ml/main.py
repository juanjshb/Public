from fastapi import FastAPI
from models import Transaccion
from detector import detectar_fraude

app = FastAPI(title="API Detección de Fraude RD",
              description="Ejemplo de cumplimiento con Ley 172-13 y 155-17")

@app.post("/analizar")
def analizar_transaccion(tx: Transaccion):
    """
    Recibe datos de una transacción bancaria,
    devuelve score de riesgo y si es sospechosa.
    """
    resultado = detectar_fraude(
        cliente_id=tx.cliente_id,
        monto=float(tx.monto),
        hora=tx.hora,
        pais=tx.pais
    )
    return {
        "fraude_sospechoso": resultado["es_fraude"],
        "score_riesgo": resultado["score"],
        "cliente_hash": resultado["cliente_hash"],  # nunca retornamos el ID original
        "pais": resultado["pais"],
        "timestamp": resultado["timestamp"]
    }
