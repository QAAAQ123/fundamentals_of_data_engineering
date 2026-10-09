CREATE TABLE Customer_staging(
    CustomerId int,
    CustomerName varchar(20),
    CustomerCountry varchar(10),
    LastUpdated timestamp
);

INSERT INTO Customer_staging (CustomerId, CustomerName, CustomerCountry, LastUpdated)
VALUES
    (100, 'Jane',  'USA', '2019-05-01 07:01:10'),
    (101, 'Bob',   'UK',  '2020-01-15 13:05:31'),
    (102, 'Miles', 'UK',  '2020-01-29 09:12:00'),
    (101, 'Jane',  'UK',  '2020-06-20 08:15:34');