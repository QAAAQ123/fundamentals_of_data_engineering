import sys
import psycopg2
import configparser

def connect_to_warehouse():
    # conf 파일로부터 db 연결 파라미터 가져오기
    parser = configparser.ConfigParser()
    parser.read("pipeline.conf")
    dbname = parser.get("aws_creds", "database")
    user = parser.get("aws_creds", "username")
    password = parser.get("aws_creds", "password")
    host = parser.get("aws_creds", "host")
    port = parser.get("aws_creds", "port")

    # Redshift 클러스터에 연결
    rs_conn = psycopg2.connect(
        "dbname=" + dbname
        + " user=" + user
        + " password=" + password
        + " host=" + host
        + " port=" + port
    )

    return rs_conn

# 두 개의 스크립트와 비교 연산자로 이루어진 테스트를 수행
# pass/fail 테스트에 대해 true/false를 반환
def execute_test(
    db_conn,
    script_1,
    script_2,
    comp_operator):

    # 첫 번째 스크립트를 실행하고 결과를 저장
    cursor = db_conn.cursor()
    sql_file = open(script_1, 'r')
    cursor.execute(sql_file.read())

    record = cursor.fetchone()
    result_1 = record[0]
    db_conn.commit()
    cursor.close()


    # 두 번째 스크립트를 실행하고 결과를 저장
    cursor = db_conn.cursor()
    sql_file = open(script_2, 'r')
    cursor.execute(sql_file.read())

    record = cursor.fetchone()
    result_2 = record[0]
    db_conn.commit()
    cursor.close()

    print("result 1 = " + str(result_1))
    print("result 2 = " + str(result_2))

    # comp_operator 값을 기반으로 비교
    if comp_operator == "equals":
        return result_1 == result_2
    elif comp_operator == "greater_equals":
        return result_1 >= result_2
    elif comp_operator == "greater":
        return result_1 > result_2
    elif comp_operator == "less_equals":
        return result_1 <= result_2
    elif comp_operator == "less":
        return result_1 < result_2
    elif comp_operator == "not_equal":
        return result_1 != result_2

    return False

def log_result(
    db_conn,
    script_1,
    script_2,
    comp_operator,
    result):
    m_query = """INSERT INTO 
                    validation_run_history(
                        script_1,
                        script_2,
            comp_operator,
            test_result,
            test_run_at)
VALUES(%s, %s, %s, %s,
    current_timestamp);"""

    m_cursor = db_conn.cursor()
    m_cursor.execute(
        m_query,
        (script_1,
        script_2,
        comp_operator,
        result)
    )

    db_conn.commit()

    m_cursor.close()
    db_conn.close()

    return

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--h":
        print("Usage: python validator.py"
            + " script1.sql script2.sql "
            + "comparison_operator")
        print("Valid comparison_operator values:")
        print("equals")
        print("greater_equals")
        print("greater")
        print("less_equals")
        print("less")
        print("not_equal")

    exit(0)