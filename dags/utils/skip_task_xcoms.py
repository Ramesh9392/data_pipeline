def push_skipped_xcoms(**kwargs):
    ti = kwargs['ti']
    ti.xcom_push(key='status', value='skipped')
    ti.xcom_push(key='notes', value='Skipped due to branch condition')
    ti.xcom_push(key='retry_count', value=ti.try_number)
    ti.xcom_push(key='start_time', value=datetime.utcnow().isoformat())
    ti.xcom_push(key='end_time', value=datetime.utcnow().isoformat())