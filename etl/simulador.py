import json, os, random
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=-5))                    # hora de Colombia
inicio = datetime(2026, 10, 5, 6, 0, tzinfo=TZ)
os.makedirs("../data", exist_ok=True)

# Creamos las lecturas
lecturas_generadas = 0
with open("../data/lecturas.jsonl", "w", encoding="utf-8") as f:
    for device_id in [1, 2]:                              # Dos dispositivos como pide la guía
        for i in range(144):                              # 12 h, una lectura cada 5 min
            msg = {
                "device_id": device_id,
                "ts": (inicio + timedelta(minutes=5 * i)).isoformat(),
                "p_ac": round(random.uniform(0, 5.0), 3),          # kW
                "irradiancia": round(random.uniform(0, 1000), 1),  # W/m2
                "temp_modulo": round(random.uniform(18, 60), 1),   # grados C
                "voltaje_dc": round(random.uniform(300, 400), 1)   # CAMPO NUEVO AGREGADO (Paso 1)
            }
            if random.random() < 0.03:
                msg["alarma"] = "GRID_FAULT"
            f.write(json.dumps(msg) + "\n")
            lecturas_generadas += 1

print(f"Éxito: Se generaron {lecturas_generadas} lecturas en la carpeta data/lecturas.jsonl")
