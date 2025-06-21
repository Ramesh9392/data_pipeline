from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.empty import EmptyOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import os

# Module imports
from ingestion.api_fetcher.fetch_random_user import fetch_random_product
from storage.postgres_loader.write_to_postgres import write_to_postgres
from utils.branch_decision import evaluate_data_count
from utils.skip_task_xcoms import push_skipped_xcoms

# Receiver emails
receiver_email = os.getenv('receiver_email', '')
receiver_email_list = [email.strip() for email in receiver_email.split(',') if email.strip()]

# Load email HTML template
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'utils', 'email_content_template.html')
with open(TEMPLATE_PATH, 'r') as f:
    html_template = f.read()

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': receiver_email_list,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2025, 6, 20),
}

# DAG definition
with DAG(
    dag_id='random_user_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['trigger rule', 'branching', 'e-mail', 'task_instance', 'sensors', 'Operators']
) as dag:

    wait_for_existing_data = SqlSensor(
        task_id='wait_for_existing_data',
        conn_id='postgres_default',
        sql='sql/check_fresh_data.sql',
        mode='poke',
        poke_interval=30,
        timeout=120,
    )

    branch_task = BranchPythonOperator(
        task_id='branch_on_count',
        python_callable=evaluate_data_count,
        provide_context=True,
    )

    fetch_task = PythonOperator(
        task_id='fetch_random_product',
        python_callable=fetch_random_product,
    )

    insert_task = PythonOperator(
        task_id='insert_postgres',
        python_callable=write_to_postgres,
        op_args=['{{ ti.xcom_pull(task_ids="fetch_random_product") }}'],
        provide_context=True,
    )

    audit_task = PostgresOperator(
        task_id='log_ingestion_audit',
        postgres_conn_id='postgres_default',
        sql='sql/log_ingestion.sql',
        #trigger_rule=TriggerRule.ALWAYS,
    )

    skip_task = PythonOperator(
        task_id='skip_fetch_insert',
        python_callable=push_skipped_xcoms
    )

    email_summary = EmailOperator(
        task_id='send_summary_email',
        to=receiver_email_list,
        subject='[Airflow] Random Product Ingestion Report - {{ ds }}',
        html_content=html_template,
        #trigger_rule=TriggerRule.ALL_DONE,
    )

    join_task = EmptyOperator(
        task_id='join_branches',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS  # Waits for all, proceeds if at least one success
    )

    # Define the flow
    wait_for_existing_data >> branch_task
    branch_task >> fetch_task >> insert_task >> join_task
    branch_task >> skip_task >> join_task

    join_task >> audit_task >> email_summary