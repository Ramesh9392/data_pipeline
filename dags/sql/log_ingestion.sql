-- Create the ingestion_audit table if it doesn't exist
CREATE TABLE IF NOT EXISTS ingestion_audit (
    id SERIAL PRIMARY KEY,
    ingestion_date DATE,
    source TEXT,
    record_count INTEGER,
    status TEXT,
    notes TEXT,
    retry_count INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- Insert audit log
INSERT INTO ingestion_audit (
    ingestion_date,
    source,
    record_count,
    status,
    notes,
    retry_count,
    start_time,
    end_time
)
VALUES (
    '{{ ds }}',
    'random_product_api',
    {{ ti.xcom_pull(task_ids='insert_postgres', key='record_count') or 0 }},
    '{{ ti.xcom_pull(task_ids="insert_postgres", key="status") or "skipped" }}',
    '{{ ti.xcom_pull(task_ids="insert_postgres", key="notes") or "Task Skipped" }}',
    {{ ti.xcom_pull(task_ids="insert_postgres", key="retry_count") or 0 }},
    {{ ("'" ~ ti.xcom_pull(task_ids="insert_postgres", key="start_time") ~ "'::timestamp") if ti.xcom_pull(task_ids="insert_postgres", key="start_time") else "NULL" }},
    {{ ("'" ~ ti.xcom_pull(task_ids="insert_postgres", key="end_time") ~ "'::timestamp") if ti.xcom_pull(task_ids="insert_postgres", key="end_time") else "NULL" }}
);
