CREATE TABLE IF NOT EXISTS validator_summary_daily(
    test_date DATE,
    script_1 VARCHAR(255),
    script_2 VARCHAR(255),
    comp_operator VARCHAR(10),
    test_composite_name VARCHAR(650),
    test_result VARCHAR(20),
    test_count int
);

TRUNCATE TABLE validator_summary_daily;

INSERT INTO validator_summary_daily
    (test_date, script_1, script_2, comp_operator,
    test_composite_name, test_result, test_count)
SELECT
    CAST(test_run_at AS DATE) AS test_date,
    script_1,
    script_2,
    comp_operator,
        (script_1
        || ' '
        || script_2
        || ' '
        || comp_operator) AS test_composite_name,
    test_result,
    COUNT(*) AS test_count
FROM validation_run_history
GROUP BY
    CAST(test_run_at AS DATE),
    script_1,
    script_2,
    comp_operator,
    (script_1 || ' ' || script_2 || ' ' || comp_operator),
    test_result;