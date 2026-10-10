CREATE TABLE Orders_cdc
(
    EventType varchar(20),
    OrderId int,
    OrderStatus varchar(20),
    LastUpdated timestamp
);

INSERT INTO Orders_cdc (EventType, OrderId, OrderStatus, LastUpdated)
VALUES
    ('insert', 1, 'Backordered', '2020-06-01 12:00:00'),
    ('update', 1, 'Shipped',     '2020-06-09 12:00:25'),
    ('delete', 1, 'Shipped',     '2020-06-10 09:05:12'),
    ('insert', 2, 'Backordered', '2020-07-01 09:05:12'),
    ('update', 2, 'Shipped',     '2020-07-09 12:15:12'),
    ('delete', 3, 'Backordered', '2020-07-11 13:10:12');