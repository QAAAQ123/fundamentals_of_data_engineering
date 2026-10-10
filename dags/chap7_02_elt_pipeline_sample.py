import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id = 'elt_pipeline_sample',
    description="A sample ELT pipeline",
    schedule="@daily",
    start_date=pendulum.today("UTC").add(days=-1),
    catchup=False,
) as dag:

    extract_orders_task = BashOperator(
        task_id="extract_order_data",
        bash_command="python /p/extract_orders.py",
    )

    extract_customers_task = BashOperator(
        task_id="extract_customer_data",
        bash_command="python /p/extract_customers.py",
    )

    load_orders_task = BashOperator(
        task_id="load_order_data",
        bash_command="python /p/load_orders.py",
    )

    load_customers_task = BashOperator(
        task_id="load_customer_data",
        bash_command="python /p/load_customers.py",
    )

    revenue_model_task = SQLExecuteQueryOperator(
        task_id="build_data_model",
        conn_id='redshift_dw',
        sql='/sql/order_revenue_model.sql',
    )

    extract_orders_task>>load_orders_task>>revenue_model_task
    extract_customers_task>>load_customers_task>>revenue_model_task