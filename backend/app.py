import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="ADM%698#",
        host="158.170.66.234",
        port="5432"
    )

@app.route('/api/indicadores')
def indicadores():
    conn = get_connection()
    df = pd.read_sql("SELECT anho, COUNT(*) AS total FROM ad.matriculas GROUP BY anho ORDER BY anho", conn)
    conn.close()
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/pronosticos')
def pronosticos():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM ad.forecast ORDER BY anho", conn)
    conn.close()
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

