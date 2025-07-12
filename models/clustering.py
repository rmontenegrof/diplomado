import pandas as pd
from sklearn.cluster import KMeans
import psycopg2

# === 1. Cargar datos ===
df = pd.read_csv('/opt/p_mat/data/matriculas_limpias.csv')

# === 2. Crear tabla dinámica ===
pivot = df.pivot(index='carrera', columns='anho', values='matriculas').fillna(0)

# === 3. Aplicar KMeans ===
kmeans = KMeans(n_clusters=3, random_state=0)
pivot['cluster'] = kmeans.fit_predict(pivot)

# === 4. Guardar en CSV ===
output_path = '/opt/p_mat/data/clusters.csv'
pivot.reset_index()[['carrera', 'cluster']].to_csv(output_path, index=False)
print(f"✅ Clusters generados y guardados en {output_path}")

# === 5. Insertar en base de datos postgres, tabla ad.clusters ===
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="postgres",
    user="postgres",
    password="ADM%698#"
)
cur = conn.cursor()

# Limpiar tabla primero
cur.execute("TRUNCATE ad.clusters")

# Insertar datos
for _, row in pivot.reset_index()[['carrera', 'cluster']].iterrows():
    cur.execute("""
        INSERT INTO ad.clusters (carrera, cluster)
        VALUES (%s, %s)
        ON CONFLICT (carrera) DO UPDATE SET cluster = EXCLUDED.cluster
    """, (row['carrera'], int(row['cluster'])))

conn.commit()
cur.close()
conn.close()
print("✅ Clusters insertados en ad.clusters")

