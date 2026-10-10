CREATE TABLE orders_time_to_ship(
    OrderId int,
    backordered_days interval
);

INSERT INTO orders_time_to_ship
    (OrderId, backordered_days)
WITH o_backordered_days AS
(
    SELECT
        OrderId,
        MIN(LastUpdated) AS first_backordered
    FROM Order_cdc
    WHERE OrderStatus = 'Backordered'
    GROUP BY OrderId
),
o_shipped AS
(
    SELECT
        OrderId,
        MIN(LastUpdated) AS first_shipped
    FROM Order_cdc
    WHERE OrderStatus = 'Shipped'
    GROUP BY OrderId
)
SELECT 
    b.OrderId,
    first_shipped - first_backordered
        AS backordered_days
FROM o_backorder AS b
INNER JOIN o_shipped AS s
    ON s.OrderId = b.OrderId

-- 전환 평균 시간 확인 하는 SQL
SELECT AVG(backordered_days)
FROM order_time_to_ship;