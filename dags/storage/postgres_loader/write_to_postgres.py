import os
import json
import ast
import psycopg2
from datetime import datetime

def write_to_postgres(data, **kwargs):
    ti = kwargs.get('ti')
    start_time = datetime.utcnow()
    inserted_count = 0
    error_message = None
    products = []

    # Parse input
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(data)
            except Exception as e:
                error_message = f"Invalid input format: {str(e)}"
                data = {}

    if not data or 'data' not in data or not isinstance(data['data'], list):
        error_message = error_message or "No valid product data found."
        data = {'data': []}

    products = data['data']
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB'),
        )
        cur = conn.cursor()

        # Create table if needed
        cur.execute("""CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            description TEXT,
            ean TEXT,
            upc TEXT,
            image TEXT,
            net_price DECIMAL,
            taxes DECIMAL,
            price DECIMAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        for product in products:
            cur.execute("""INSERT INTO products (
                name, description, ean, upc, image, net_price, taxes, price, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                product.get('name'),
                product.get('description'),
                product.get('ean'),
                product.get('upc'),
                product.get('image'),
                float(product.get('net_price', 0) or 0),
                float(product.get('taxes', 0) or 0),
                float(product.get('price', 0) or 0),
                datetime.utcnow()
            ))
            inserted_count += 1

        conn.commit()

    except Exception as e:
        error_message = str(e)
        if conn:
            conn.rollback()

    finally:
        end_time = datetime.utcnow()

        if cur:
            cur.close()
        if conn:
            conn.close()

        # Always push audit info
        if ti:
            ti.xcom_push(key='record_count', value=inserted_count)
            ti.xcom_push(key='status', value='success' if inserted_count > 0 and not error_message else 'failure')
            ti.xcom_push(key='notes', value='Inserted successfully' if not error_message else error_message)
            ti.xcom_push(key='retry_count', value=ti.try_number)
            ti.xcom_push(key='start_time', value=start_time.isoformat())
            ti.xcom_push(key='end_time', value=end_time.isoformat())

    # Re-raise the error to let Airflow mark the task as failed
    if error_message:
        raise Exception(error_message)
