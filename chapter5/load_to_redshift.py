"""
AWS Redshift 계정 없이 로컬 저장과 DuckDB로 대체


import configparser
import psycopg2

parser = configparser.ConfigParser()
parser.read("pipeline.conf")

#red shift 연결
red_shshift_conn = psycopg2.connect()
#account_id 및 iam_role 로드
iam_role = parser.get("xxx", "iam_role")
acc_id = parser.get("xxx", "account_id")
bucket_name = parser.get("xxx", "bucket_name")

file_path = ("s3://"
    + bucket_name
    + "/order_extract.csv")
role_string = ("arn:aws:iam::"
    + acc_id
    + ":role" + iam_role)

sql = "COPY public.Orders"
sql = sql + " from %s "
sql = sql + " iam_rolw %s;"

# cursor 객체 생성 및 COPY 실행
cur = red_shshift_conn.cursor()
cur.execute(sql, (file_path, role_string))

# cursor 종료 후 트랜잭션 커밋
cur.close()
red_shshift_conn.commit()

red_shshift_conn.close()
"""

"""
1. DuckDB 연결
2. 적재할 테이블 작성 => chap4의 data/orders.csv가 S3에 들어가 있다고 가정
3. CSV → DuckDB 적재 SQL 작성
4. 적재 실행
5. DuckDB 연결 종료

"""
from pathlib import Path

import duckdb

# 1. 연결
conn_duck = duckdb.connect(":memory:")

# csv 불러오기(S3)
root_path = Path(__file__).resolve().parents[1]
order_csv = Path(root_path / "chapter4" / "data" / "orders.csv")

# 테이블 생성
create_table_sql = f"""
    CREATE TABLE Orders(
        OrderId int,
        OrderStatus varchar(30),
        LastUpdated timestamp
    );
"""
conn_duck.execute(create_table_sql)

# COPY 실행(SnowFlake는 COPY INTO)
sql = f"""
    COPY Orders
    FROM '{order_csv}'
"""
conn_duck.execute(sql)

rows = conn_duck.execute("SELECT * FROM Orders").fetchall()
print(f"Duck DB Orders 테이블 필드: {rows}")

conn_duck.close()

