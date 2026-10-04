-- Paso 6: Gobernanza aplicada (Rol de lectura)

-- Eliminamos el rol si ya existe (para evitar errores si ejecutas el script de nuevo)
DROP ROLE IF EXISTS solar_lector;

-- Creamos el rol con una contraseña
CREATE ROLE solar_lector LOGIN PASSWORD 'lector_pass';

-- Le damos acceso a la base de datos y al esquema
-- (Asumiendo que estás conectado a tu base de datos)
GRANT USAGE ON SCHEMA public TO solar_lector;

-- Le damos permiso ÚNICAMENTE de lectura (SELECT) sobre la tabla
GRANT SELECT ON lectura_demo TO solar_lector;

-- Prueba (para tomar la captura):
-- 1. Abre otra ventana de psql o conexión en pgAdmin usando el usuario 'solar_lector'
-- 2. Haz: SELECT * FROM lectura_demo LIMIT 5; (Esto DEBE funcionar)
-- 3. Haz: INSERT INTO lectura_demo (dispositivo_id, ts) VALUES (99, now()); (Esto DEBE fallar)
