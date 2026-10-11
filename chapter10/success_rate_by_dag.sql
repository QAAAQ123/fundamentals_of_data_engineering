SELECT 
    dag_id,
    SUM(
            CASE WHEN dag_state = 'success' THEN 1
            ELSE 0 
            END
        ) / CAST(SUM(dag_run_count) AS DECIMAL(6, 2))
    AS success_rate
FROM dag_history_daily
GROUP BY dag_id;