import os
import json
import psycopg2
from datetime import datetime

# =====================================================================
# ATENCIÓN: Cambia 'tu_contraseña' por la contraseña que le pusiste a
# PostgreSQL durante la instalación.
# =====================================================================
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "tu_contraseña"
DB_PORT = "5432"

def run_etl():
    print("--- Iniciando proceso ETL ---")
    
    # 1. Crear conexión
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        cur = conn.cursor()
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return

    # Registrar inicio en la bitácora
    cur.execute("INSERT INTO etl_log (estado) VALUES ('EN_CURSO') RETURNING id;")
    log_id = cur.fetchone()[0]
    conn.commit()

    try:
        # 2. Cargar datos JSONL a la tabla staging (Paso 2)
        print("Cargando datos a stg_lectura_raw...")
        filepath = os.path.join(os.path.dirname(__file__), "../data/lecturas.jsonl")
        filas_leidas = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    cur.execute("INSERT INTO stg_lectura_raw (payload) VALUES (%s)", (line.strip(),))
                    filas_leidas += 1
        
        # 3. Transformar y cargar a lectura_demo con idempotencia (Paso 3)
        print("Transformando e insertando en lectura_demo...")
        with open(os.path.join(os.path.dirname(__file__), "../sql/02_carga.sql"), "r", encoding='utf-8') as sql_file:
            query = sql_file.read()
            cur.execute(query)
            # En PostgreSQL, rowcount nos dice cuántas filas se afectaron (insertaron)
            filas_cargadas = cur.rowcount
            
        filas_rechazadas = filas_leidas - filas_cargadas

        # 4. Actualizar bitácora (Paso 5)
        print("Actualizando bitácora...")
        cur.execute("""
            UPDATE etl_log 
            SET fin = now(), 
                filas_leidas = %s, 
                filas_cargadas = %s, 
                filas_rechazadas = %s, 
                estado = 'EXITO' 
            WHERE id = %s
        """, (filas_leidas, filas_cargadas, filas_rechazadas, log_id))
        
        conn.commit()
        print(f"ETL completado exitosamente. Leídas: {filas_leidas}, Cargadas: {filas_cargadas}, Ignoradas (Duplicadas): {filas_rechazadas}")

    except Exception as e:
        conn.rollback()
        print(f"Error durante el ETL: {e}")
        cur.execute("""
            UPDATE etl_log 
            SET fin = now(), estado = 'ERROR', mensaje_error = %s 
            WHERE id = %s
        """, (str(e), log_id))
        conn.commit()

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_etl()
