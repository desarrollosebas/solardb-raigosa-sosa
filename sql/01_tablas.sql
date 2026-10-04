-- Paso 2: Creación de tablas de staging y destino

DROP TABLE IF EXISTS stg_lectura_raw;
CREATE TABLE stg_lectura_raw (
  id          BIGSERIAL PRIMARY KEY,
  payload     JSONB NOT NULL,
  cargado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

DROP TABLE IF EXISTS lectura_demo;
CREATE TABLE lectura_demo (
  dispositivo_id INT NOT NULL,
  ts             TIMESTAMPTZ NOT NULL,
  p_ac           NUMERIC(10,3) CHECK (p_ac >= 0),
  irradiancia    NUMERIC(8,1)  CHECK (irradiancia BETWEEN 0 AND 1500),
  temp_modulo    NUMERIC(5,1),
  payload        JSONB,
  PRIMARY KEY (dispositivo_id, ts)
);

-- Paso 5: Creación de la tabla de bitácora
DROP TABLE IF EXISTS etl_log;
CREATE TABLE etl_log (
    id               SERIAL PRIMARY KEY,
    inicio           TIMESTAMPTZ NOT NULL DEFAULT now(),
    fin              TIMESTAMPTZ,
    filas_leidas     INT DEFAULT 0,
    filas_cargadas   INT DEFAULT 0,
    filas_rechazadas INT DEFAULT 0,
    estado           VARCHAR(20) NOT NULL DEFAULT 'EN_CURSO',
    mensaje_error    TEXT
);
