"""
DWH에 DAG 실행 기록 로드하는 파일
"""

import boto3
import configparser
import psycopg2

# db Redshift 연결 정보 가져오기
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
dbname = parser.get("aws_creds", "database")
user = parser.get("aws_creds", "username")
password = parser.get("aws_creds", "password") 
host = parser.get("aws_creds", "host")
port = parser.get("aws_creds", "port")

# redshift 클러스터에 연결
rs_conn = psycopg2.connect( "dbname=" + dbname
    + " user=" + user
    + " password=" + password
    + " host=" + host
    + " port=" + port)

# 구성 파일에서 account_id와 iam_role을 로드
parser = configparser.ConfigParser()
parser.read("pipeline.conf")

account_id = parser.get(
    "aws_boto_credentials",
    "account_id")
iam_role = parser.get("aws_creds", "iam_role")

# Redshift로 가져오기 위해 COPY command를 실행
file_path = "s3://bucket-name/dag_run_extract.csv"

sql = """COPY dag_run_history
    (id,dag_id,execution_date,
    state,run_id,external_trigger,
    end_date,start_date)"""
sql = sql + " from %s "
sql = sql + " iam_role 'arn:aws:iam::%s:role/%s';"

# cursor 객체를 생성하고 COPY command를 실행
cur = rs_conn.cursor()
cur.execute(sql, (file_path, account_id, iam_role))

# cursor를 종료하고 트랜잭션을 저장
cur.close()
rs_conn.commit()

# 연결을 종료
rs_conn.close()