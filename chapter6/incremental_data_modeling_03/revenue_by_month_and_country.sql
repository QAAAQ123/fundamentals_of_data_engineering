SELECT 
    DATE_PART('month', order_date) AS order_month, order_country,
    SUM(total_revenue) AS order_revenue
FROM order_summary_daily_current
GROUP BY
    DATE_PART('month', order_date),
    order_country
ORDER BY
    DATE_PART('month', order_date),
    order_country