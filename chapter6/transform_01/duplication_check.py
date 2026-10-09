import configparser
from pathlib import Path

from duckdb import connect
import psycopg2

base_dir = Path(__file__).resolve().parent

if __name__ == "__main__":
    print("1. config 읽기")

    parser = configparser.ConfigParser()
    parser.read("pipeline.conf")

    dbname = parser.get("postgres_config", "database")
    user = parser.get("postgres_config", "username")
    password = parser.get("postgres_config", "password")
    host = parser.get("postgres_config", "host")
    port = parser.get("postgres_config", "port")

    print("2. PostgreSQL 연결 중...")

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
        connect_timeout=5
    )

    print("3. PostgreSQL 연결 성공")

    creation_orders = """
    DROP TABLE IF EXISTS Orders;

    CREATE TABLE Orders(
        OrderId int,
        OrderStatus varchar(30),
        LastUpdated timestamp
    );
    """
    insertion_orders_data = """
    INSERT INTO Orders
    VALUES
        (1, 'Backordered', '2020-06-01'),
        (2, 'Shipped', '2020-06-02'),
        (3, 'Pending', '2020-06-03'),
        (4, 'Delivered', '2020-06-04'),
        (5, 'Cancelled', '2020-06-05'),
        (6, 'Processing', '2020-06-06'),
        (7, 'Returned', '2020-06-07'),
        (1, 'Backordered', '2020-06-01'),
        (9, 'Shipped', '2020-06-02'),
        (10, 'Pending', '2020-06-08');
    """

    check_dup = """
    SELECT *,
        COUNT(1) AS dup_count
    FROM Orders
    GROUP BY OrderId, OrderStatus, LastUpdated
    HAVING COUNT(1) > 1;
    """

    m_cursor = conn.cursor()

    try:
        m_cursor.execute(creation_orders)
        m_cursor.execute(insertion_orders_data)
        conn.commit()
        m_cursor.execute("SELECT * FROM Orders")
        result = m_cursor.fetchall()
        print(f"전체 값: {result}")
    except Exception:
        conn.rollback()
        raise

    m_cursor.execute(check_dup)
    result = m_cursor.fetchall()

    print(f"dup 확인: {result}")

    m_cursor.close()
    conn.close()