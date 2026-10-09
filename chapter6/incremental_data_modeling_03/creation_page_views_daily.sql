-- 일별, 국가별로 페이지뷰 수를 보여주는 테이블
CREATE TABLE pageviews_daily(
    view_date date,
    url_path varchar(250),
    customer_country varchar(50),
    view_count int
);

INSERT INTO pageviews_daily
    (view_date, url_path, customer_country, view_count)
SELECT 
    CAST(p.ViewTime AS Date) AS view_date,
    p.UrlPath AS url_path,
    c.CustomerCountry AS customer_countrh,
    COUNT(*) AS view_count
FROM PageViews AS p
LEFT JOIN Customers AS c
    ON c.CustomerId = p.CustomerId
GROUP BY
    CAST(p.ViewTime AS Date)
    p.UrlPath,
    c.CustomerCountry