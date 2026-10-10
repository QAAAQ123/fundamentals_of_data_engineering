import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.sensors.external_task import ExternalTaskSensor
from airflow.providers.standard.operators.empty import EmptyOperator

with DAG(
    dag_id="sensor_test",
    description="DAG with a sensor",
    schedule="0 0 1 * *",
    start_date=pendulum.datetime(2026, 11, 10, tz="Asia/Seoul"),
    catchup=False,
) as dag:

    sensor1 = ExternalTaskSensor(
        task_id="dag_sensor",
        external_dag_id="elt_pipeline_sample",#모니터링할 대상
        external_task_id=None,#None: elt pipeline sample이 성공할 때까지 기다림
        mode="reschedule",
        timeout=2500, #외부 종속성(elt pipeline sample을 지켜보는 시간)
    )

    task1 = EmptyOperator(
        task_id="dummy_task",
        retries=1,
    )

    sensor1 >> task1