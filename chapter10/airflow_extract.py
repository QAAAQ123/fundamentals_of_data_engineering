"""
DAG 실행 기록을 수집하는 파일
"""
import csv
import boto3
import configparser
import psycopg2

# db Redshift에서 연결 정보 가져오기
parser = configparser.ConfigParser()
dbname = parser.get("aws_creds", "database")
user = parser.get("aws_creds", "username")
password = parser.get("aws_creds", "password")
host = parser.get("aws_creds", "host")
port = parser.get("aws_creds", "port")

# redshift 클러스터에 연결
rs_conn = psycopg2.connect(
    "dbname=" + dbname
    + " user=" + user
    + " password=" + password
    + " host=" + host
    + " port=" + port
)

rs_sql = """SELECT COALESCE(MAX(id),-1)
FROM dag_run_history;"""

rs_cursor = rs_conn.cursor()
rs_cursor.execute(rs_sql)
result = rs_cursor.fetchone()

# 하나의 결과 행이 반환
last_id = result[0]
rs_cursor.close()
rs_conn.commit()

# airflow db에 연결
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
dbname = parser.get("airflowdb_config", "database")
user = parser.get("airflowdb_config", "username")
password = parser.get("airflowdb_config", "password")
host = parser.get("airflowdb_config", "host")
port = parser.get("airflowdb_config", "port")


conn = psycopg2.connect(
+ " password=" + password
    + " host=" + host
    + " port=" + port)

# 새로운 DAG 하나를 조회. 실행 중인 DAG는 무시
m_query = """SELECT
    id,
    dag_id,
    execution_date,
    state,
    run_id,
    external_trigger,
    end_date,
    start_date

FROM dag_run
WHERE id > %s
AND state <> 'running';
"""

m_cursor = conn.cursor()
m_cursor.execute(m_query, (last_id,))
results = m_cursor.fetchall()

local_filename = "dag_run_extract.csv"
with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp, delimiter='|')
    csv_w.writerows(results)

fp.close()
m_cursor.close()
conn.close()

# _boto_credentials 값을 로드
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
access_key = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
bucket_name = parser.get("aws_boto_credentials", "bucket_name")


# 로컬 CSV를 S3 버킷에 업로드
s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)
s3_file = local_filename
s3.upload_file(local_filename, bucket_name, s3_file)