import psycopg2
import pandas as pd

# 1. Extraer datos desde consolidado_externo."SAI".vrep_matriculas_dei
source_conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="consolidado_externo",
    user="postgres",
    password="ADM%698#"
)

query = """
    SELECT
        left(periodo_matricula,4) as anio,
        cod_carr_prog AS carrera,
        sexo,
        via_ingreso,
        COUNT(distinct rut_usach) AS matriculas
    FROM "SAI".vrep_matriculas_dei vmd
    LEFT JOIN cpp_vw cv
  ON cv.cod_pla = vmd.cod_plan
 AND cv.anho_plan = CAST(LEFT(vmd.periodo_matricula, 4) AS INT)
WHERE cod_unidad != 150
  AND nivel_global = 'Pregrado'
    GROUP BY left(periodo_matricula,4), cod_carr_prog, sexo, via_ingreso
    ORDER BY left(periodo_matricula,4), cod_carr_prog;
"""

df = pd.read_sql(query, source_conn)
source_conn.close()

# 2. Guardar como CSV
df.to_csv("../data/matriculas.csv", index=False)

# 3. Insertar en la tabla ad.matriculas de la base de datos postgres
target_conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="ADM%698#"
)
cursor = target_conn.cursor()

# Limpiar tabla antes de insertar
cursor.execute("TRUNCATE ad.matriculas")

# Insertar fila por fila
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO ad.matriculas (anho, carrera, sexo, via_ingreso, matriculas)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['anio'], row['carrera'], row['sexo'], row['via_ingreso'], row['matriculas']))

target_conn.commit()
cursor.close()
target_conn.close()

print("ETL finalizado: datos cargados en ad.matriculas y CSV generado.")

