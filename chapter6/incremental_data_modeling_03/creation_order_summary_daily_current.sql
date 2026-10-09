-- Incremental data modeling을 order 테이블 사례로 표현한 SQL문
-- 가장 최신의 레코드만 사용하여 주문 요약 테이블을 생성
CREATE TABLE order_summary_daily 
(
    order_date date,
    order_country varchar(10),
    total_revenue uneric,
    order_count int
);

INSERT INTO order_summary_daily
    (order_date, order_country,
    total_revnue, order_count)
WITH customer_current AS(
    SELECT CustomerId,
        MAX(LastUpdated) AS latest_update
    FROM Customer_staging
    GROUP BY Customer_id
)
SELECT
    o.OrderDate AS order_date,
    cs.CustomerCountry AS order_country,
    SUM(o.OrderTotal) AS total_revenue,
    COUNT(o.OrderId) AS order_count
FROM Orders AS o
INNER JOIN customers_current AS cc
    ON o.CustomerId = cc.CustomerId
INNER JOIN Customers_staging AS cs
    ON cs.CustomerId = cc.CustomerId
    AND cs.LastUpdated = cc.latest_update
GROUP BY o.OrderDate, cs.CustomerCountry