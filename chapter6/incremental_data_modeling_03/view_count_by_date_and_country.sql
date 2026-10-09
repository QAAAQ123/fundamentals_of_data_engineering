SELECT 
    view_date,
    customer_country,
    SUM(view_count)
FROM pageviews_daily
GROUP BY view_date, customer_country
ORDER BY view_date, customer_country