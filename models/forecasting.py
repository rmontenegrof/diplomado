import pandas as pd
from prophet import Prophet
import psycopg2

# === 1. Leer datos de matrícula ===
df = pd.read_csv('/opt/p_mat/data/matriculas_limpias.csv')

# === 2. Seleccionar una carrera para el pronóstico ===
carrera_elegida = df['carrera'].unique()[0]  # puedes reemplazarlo por una carrera fija si quieres
df_filtrada = df[df['carrera'] == carrera_elegida][['anho', 'matriculas']].copy()

# === 3. Preparar datos para Prophet ===
df_filtrada.rename(columns={'anho': 'ds', 'matriculas': 'y'}, inplace=True)
df_filtrada['ds'] = pd.to_datetime(df_filtrada['ds'], format='%Y')

# === 4. Entrenar modelo ===
modelo = Prophet()
modelo.fit(df_filtrada)

# === 5. Hacer predicciones ===
futuro = modelo.make_future_dataframe(periods=3, freq='Y')
forecast = modelo.predict(futuro)
result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# === 6. Guardar a CSV ===
output_path = '/opt/p_mat/data/forecast.csv'
result.to_csv(output_path, index=False)
print(f"✅ Pronóstico guardado en {output_path}")

# === 7. Insertar en tabla ad.forecast ===
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="postgres",
    user="postgres",
    password="ADM%698#"
)
cur = conn.cursor()

# Limpiar tabla antes de insertar
cur.execute("TRUNCATE ad.forecast")

# Insertar predicciones
for _, row in result.iterrows():
    cur.execute("""
        INSERT INTO ad.forecast (ds, yhat, yhat_lower, yhat_upper)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (ds) DO UPDATE SET
            yhat = EXCLUDED.yhat,
            yhat_lower = EXCLUDED.yhat_lower,
            yhat_upper = EXCLUDED.yhat_upper
    """, (row['ds'].date(), float(row['yhat']), float(row['yhat_lower']), float(row['yhat_upper'])))

conn.commit()
cur.close()
conn.close()
print("✅ Pronóstico insertado en ad.forecast")

