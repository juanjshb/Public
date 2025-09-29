import hashlib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime
import json
import os

# --- Entrenamiento inicial (datos ficticios para demo) ---
np.random.seed(42)
base = pd.DataFrame({
    "monto": np.random.normal(5000, 1500, 500).clip(100, None),
    "hora": np.random.randint(0, 24, 500),
})
model = IsolationForest(contamination=0.02, random_state=42)
model.fit(base[["monto","hora"]])

LOG_PATH = "auditoria/alertas.json"
os.makedirs("auditoria", exist_ok=True)

def detectar_fraude(cliente_id:str, monto:float, hora:int, pais:str) -> dict:
    # Anonimizar cliente_id según Ley 172-13
    cliente_hash = hashlib.sha256(cliente_id.encode()).hexdigest()

    features = pd.DataFrame([[monto, hora]], columns=["monto","hora"])
    pred = model.predict(features)[0]  # -1 = anomalía
    score = model.decision_function(features)[0]

    resultado = {
        "cliente_hash": cliente_hash,
        "pais": pais,
        "monto": monto,
        "hora": hora,
        "es_fraude": pred == -1,
        "score": float(score),
        "timestamp": datetime.utcnow().isoformat()
    }

    if resultado["es_fraude"]:
        _registrar_alerta(resultado)
    return resultado

def _registrar_alerta(alerta: dict):
    # Guardar alerta en log seguro
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

    with open(LOG_PATH, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append(alerta)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
