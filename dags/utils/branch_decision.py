from datetime import datetime


def evaluate_data_count(**kwargs):
    ti = kwargs['ti']
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    import os

    sql_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'check_record_count_sensor.sql')
    with open(sql_path, 'r') as f:
        sql_query = f.read()

    hook = PostgresHook(postgres_conn_id='postgres_default')
    result = hook.get_first(sql_query)
    count = result[0] if result else 0

    ti.xcom_push(key='record_count', value=count)
    ti.xcom_push(key='start_time', value=datetime.utcnow().isoformat())
    ti.xcom_push(key='retry_count', value=ti.try_number)

    if count < 150:
        return 'fetch_random_product'

    ti.xcom_push(key='status', value='skipped')
    ti.xcom_push(key='notes', value=f'Skipped fetch & insert as count = {count}')
    ti.xcom_push(key='end_time', value=datetime.utcnow().isoformat())
    return 'log_ingestion_audit'
