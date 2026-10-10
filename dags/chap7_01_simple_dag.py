from datetime import timedelta

import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="simple_dag",
    description="A simple DAG",
    schedule="0 0 1 * *",
    start_date=pendulum.datetime(2026, 11, 10, tz="Asia/Seoul"),
    catchup=False,
    #추가 파이프라인-이메일 설정
    default_args={
        "email": ["my_eamil@example.com"],
        "email_on_failure": True,
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    }
) as dag:

    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 3",
    )

    t3 = BashOperator(
        task_id="print_end",
        depends_on_past=False,
        bash_command="echo 'end'",
    )

    t1 >> t2 >> t3