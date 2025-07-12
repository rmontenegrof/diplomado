FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask pandas psycopg2-binary flask_cors

CMD ["python", "app.py"]

