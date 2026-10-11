from datetime import timedelta

import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="pipeline_performance",
    description="Performance measurement pipeline",
    schedule=timedelta(days=1),
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    catchup=False,
) as dag:

    extract_airflow_task = BashOperator(
        task_id="extract_airflow",
        bash_command="python /p/airflow_extract.py",
    )

    load_airflow_task = BashOperator(
        task_id="load_airflow",
        bash_command="python /p/airflow_load.py",
    )

    dag_history_model_task = SQLExecuteQueryOperator(
        task_id="dag_history_model",
        conn_id="redshift_dw",
        sql="sql/dag_history_daily.sql",
    )

    validation_history_model_task = SQLExecuteQueryOperator(
        task_id="validation_history_model",
        conn_id="redshift_dw",
        sql="sql/validator_summary_daily.sql",
    )

    extract_airflow_task >> load_airflow_task

    load_airflow_task >> [
        dag_history_model_task,
        validation_history_model_task,
    ]
