SELECT
    dag_id,
    execution_date,
    SUM(runtime_seconds)
    / SUM(CAST(dag_run_count as DECIMAL(6, 2)))
    AS avg_runtime
FROM dag_history_daily
WHERE
    dag_id = 'elt_pipeline_sample'
GROUP BY 
    dag_id,
    execution_date
ORDER BY
    dag_id,
    execution_date;