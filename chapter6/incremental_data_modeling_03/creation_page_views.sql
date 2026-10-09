CREATE TABLE PageViews(
    CustomerId int,
    ViewTime timestamp,
    UrlPath varchar(250),
    utm_medium varchar(50)
);

INSERT INTO PageViews (CustomerId, ViewTime, UriPath, utm_medium)
VALUES
    (100, '2020-06-01 12:00:00', '/home', 'social'),
    (100, '2020-06-01 12:00:13', '/product/2554', NULL),
    (101, '2020-06-01 12:01:30', '/product/6754', 'search'),
    (102, '2020-06-01 07:05:00', '/home', NULL),
    (101, '2020-06-01 12:00:00', '/product/2554', 'social');