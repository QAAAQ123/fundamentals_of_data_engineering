CREATE TABLE IF NOT EXISTS Customers_scd
(
    CustomerId int,
    CustomerName varchar(20),
    CustomerCountry varchar(10),
    ValidFrom timestamp,
    Expired timestamp
);

INSET INTO Customer_scd
    VALUES(100, 'Jane', 'USA', '2019-05-01 07:01:10', '2020-06-20 08:15:34');
    VALUES(100, 'Jane', 'UK', '2020-06-20 08:15:34', '2199-12-31 00:00:00');