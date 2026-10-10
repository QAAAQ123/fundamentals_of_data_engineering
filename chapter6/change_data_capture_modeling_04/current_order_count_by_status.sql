CREATE TABLE orders_current(
    order_status varchar(30),
    order_count int
);

INSERT INTO orders_current
    (order_status, order_count)
WITH o_latest AS(
    SELECT
        OrderId,
        MAX(LastUpdated) AS max_updated
    FROM Order_cdc
    GROUP BY OrderId
)
SELECT 
    o.OrderStatus,
    Count(1) AS order_count
FROM Order_cdc AS o
INNER JOIN o_latest AS ol
    ON ol.OrderId = o.OrderId
    AND ol.max_updated = o.LastUpdated
WHERE o.EventType <> 'delete'
GROUP BY o.OrderStatus;