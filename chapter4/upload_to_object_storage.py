import psycopg2
import csv
import configparser
from pathlib import Path
import shutil

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

    m_query = "SELECT * FROM Orders;"
    c_order_query = Path(base_dir / "create_order_table.sql").read_text(
        encoding="utf-8"
    )

    print("4. SQL 파일 읽기 완료")

    local_file_name = "order_extract.csv"
    s3_file = "raw/orders/orders.csv"

    m_cursor = conn.cursor()

    print("5. CREATE TABLE 실행 중...")
    m_cursor.execute(c_order_query)

    print("6. SELECT 실행 중...")
    m_cursor.execute(m_query)

    print("7. 데이터 가져오는 중...")
    result = m_cursor.fetchall()

    print(f"8. {len(result)}개 레코드 가져옴")

    with open(local_file_name, "w", newline="", encoding="utf-8") as fp:
        csv_w = csv.writer(fp, delimiter="|")
        csv_w.writerows(result)

    print("9. CSV 저장 완료")

    m_cursor.close()
    conn.close()

    destination = Path("data") / s3_file
    destination.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(local_file_name, destination)

    print(f"10. 업로드 완료: {destination}")