import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import psycopg2
from sqlalchemy import create_engine, text

# === Parámetros de conexión PostgreSQL ===
PG_USER = 'postgres'
PG_PASSWORD = 'ADM%25698#'
PG_HOST = 'localhost'
PG_PORT = '5432'
PG_DATABASE = 'postgres'

# === Conexión SQLAlchemy ===
engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')

# === Leer datos desde ad.matriculas ===
query = 'SELECT anho, carrera, sexo, via_ingreso, matriculas FROM ad.matriculas'
df = pd.read_sql(query, engine)

# === Guardar copia original para mantener glosas ===
df_original = df.copy()

# === Codificar variables categóricas solo para entrenamiento ===
le_carrera = LabelEncoder()
le_sexo = LabelEncoder()
le_via = LabelEncoder()

df['carrera_enc'] = le_carrera.fit_transform(df['carrera'])
df['sexo_enc'] = le_sexo.fit_transform(df['sexo'])
df['via_ingreso_enc'] = le_via.fit_transform(df['via_ingreso'])

# === Definir X e y ===
X = df[['anho', 'carrera_enc', 'sexo_enc', 'via_ingreso_enc']]
y = df['matriculas']

# === Separar en entrenamiento y test ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Entrenar el modelo ===
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === Evaluar el modelo ===
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse:.2f}")

# === Hacer pronósticos para 2025, 2026, 2027 ===
future_years = [2025, 2026, 2027]
unique_combinations = df_original[['carrera', 'sexo', 'via_ingreso']].drop_duplicates()
forecast_rows = []

for year in future_years:
    temp = unique_combinations.copy()
    temp['anho'] = year

    # Transformar para predicción
    temp_enc = pd.DataFrame({
        'anho': year,
        'carrera_enc': le_carrera.transform(temp['carrera']),
        'sexo_enc': le_sexo.transform(temp['sexo']),
        'via_ingreso_enc': le_via.transform(temp['via_ingreso']),
    })

    yhat = model.predict(temp_enc)
    temp['yhat'] = yhat
    forecast_rows.append(temp)

forecast_df = pd.concat(forecast_rows)

# === Insertar en la tabla ad.forecast ===
with engine.begin() as conn:
    conn.execute(text('TRUNCATE TABLE ad.forecast'))
    forecast_df.to_sql('forecast', conn, schema='ad', if_exists='append', index=False)

