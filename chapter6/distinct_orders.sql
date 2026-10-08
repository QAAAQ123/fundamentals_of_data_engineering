-- 첫번째: DISTINCT로 중복 제거
CREATE TABLE distinct_orders AS
SELECT DISTINCT *
FROM Orders;

TRUNCATE TABLE Orders;

INSERT INTO Orders
SELECT * FROM distinct_orders;

DROP TABLE distinct_orders;

--두번째 Window function으로 중복 제거
CREATE TABLE all_orders AS
SELECT *,
    ROW_NUMBER() OVER(PARTITION BY OrderId, OrderStatus, LastUpdated) AS dup_count
FROM Orders;

TRUNCATE TABLE Orders;

INSERT INTO Orders
    (OrderId, OrderStatus, LastUpdated)
SELECT 
    OrderId,
    OrderStatus, 
    LastUpdated
FROM all_orders
WHERE dup_count = 1;

DROP TABLE all_orders;