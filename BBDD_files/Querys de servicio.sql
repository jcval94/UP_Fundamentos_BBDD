-- Gestión de Seguridad --

-- 1. Conteo de Delitos por Tipo en un Municipio
SELECT OD."ID Municipio", M."alcaldia_hecho", D."Delito", COUNT(*) AS "Total Delitos"
FROM "Ocurrencia Delictiva" OD
JOIN "Municipio" M ON OD."ID Municipio" = M."ID Municipio"
JOIN "Delitos" D ON OD."ID Tipo Delito" = D."ID Tipo Delito"
GROUP BY OD."ID Municipio", M."alcaldia_hecho", D."Delito"
ORDER BY "Total Delitos" DESC;

-- 2. Promedio de Delitos por Mes
SELECT DATE_FORMAT("Momento delito", '%Y-%m') AS "Mes", COUNT(*) AS "Total Delitos"
FROM "Ocurrencia Delictiva"
GROUP BY "Mes"
ORDER BY "Mes";

-- Análisis de Competencia --

-- 3. Cantidad de Comercios por Tipo de Centro Comercial
SELECT CC."tipoCenCom", COUNT(*) AS "Total Comercios"
FROM "Comercios" C
JOIN "Centros comerciales" CC ON C."ID Centro comercial" = CC."ID Centro comercial"
GROUP BY CC."tipoCenCom"
ORDER BY "Total Comercios" DESC;

-- 4. Sectores con Menor Competencia
SELECT AE."nombre_act", COUNT(*) AS "Total Comercios"
FROM "Comercios" C
JOIN "Actividades Económicas" AE ON C."codigo_act" = AE."codigo_act"
GROUP BY AE."nombre_act"
ORDER BY "Total Comercios" ASC;

-- Identificación de Oportunidades --

-- 5. Áreas Geográficas Propicias para Expansión con Menor Competencia
SELECT C."nom_estab", M."alcaldia_hecho", COUNT(*) AS "Total Delitos"
FROM "Comercios" C
JOIN "Ocurrencia Delictiva" OD ON C."ID Municipio" = OD."ID Municipio"
JOIN "Municipio" M ON C."ID Municipio" = M."ID Municipio"
GROUP BY C."nom_estab", M."alcaldia_hecho"
ORDER BY "Total Delitos" ASC;

-- Visualización de Datos --

-- 6. Datos para Interfaz de Usuario Intuitiva
SELECT OD."Momento delito", D."Delito", M."alcaldia_hecho", F."fiscalia"
FROM "Ocurrencia Delictiva" OD
JOIN "Delitos" D ON OD."ID Tipo Delito" = D."ID Tipo Delito"
JOIN "Municipio" M ON OD."ID Municipio" = M."ID Municipio"
JOIN "Fiscalia" F ON OD."ID Fiscalía" = F."Id Fiscalía"
ORDER BY OD."Momento delito" DESC
LIMIT 10;

-- Alertas y Notificaciones --

-- 7. Alertas por Cambios Relevantes en la Seguridad
SELECT OD."Momento delito", D."Delito", M."alcaldia_hecho"
FROM "Ocurrencia Delictiva" OD
JOIN "Delitos" D ON OD."ID Tipo Delito" = D."ID Tipo Delito"
JOIN "Municipio" M ON OD."ID Municipio" = M."ID Municipio"
WHERE OD."Momento delito" > NOW() - INTERVAL 1 DAY
ORDER BY OD."Momento delito" DESC
LIMIT 5;

-- 8. Alertas por Cambios Relevantes en la Competencia
SELECT C."nom_estab", CC."tipoCenCom"
FROM "Comercios" C
JOIN "Centros comerciales" CC ON C."ID Centro comercial" = CC."ID Centro comercial"
WHERE C."fecha_alta" > NOW() - INTERVAL 7 DAY
ORDER BY C."fecha_alta" DESC
LIMIT 5;

-- Búsqueda de Delitos que Contienen una Palabra Específica en su Descripción --

-- 9. Delitos que Contienen una Palabra Específica en su Descripción
SELECT "Momento delito", "ID Delito", "ID Tipo Delito"
FROM "Ocurrencia Delictiva"
WHERE "Momento delito" > NOW() - INTERVAL 30 DAY
AND "Delito" REGEXP 'Robo|Hurto'; -- Puedes cambiar 'Robo|Hurto' por la palabra que desees buscar
ORDER BY "Momento delito" DESC
LIMIT 10;
