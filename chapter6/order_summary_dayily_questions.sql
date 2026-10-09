-- 특정 월, 특정 국가에서 발생한 수익은 얼마인가?
SELECT
    DATE_PART('month', order_date) AS order_month,
    order_country,
    SUM(total_revenue) AS order_revenue
FROM order_summary_dily
GROUP BY
    DATE_PART('month', order_date),
    order_country
ORDER BY
    DATE_PART('month', order_date),
    order_country;

-- 특정 날짜에 주문이 몇 개나 들어왔는가?
SELECT
    order_date,
    SUM(order_count) AS total_orders
FROM order_summary_dily
GROUP BY order_date
ORDER BY order_date;