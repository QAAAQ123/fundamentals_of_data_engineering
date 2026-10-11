"""
## 검증 테스트 실행 방법 예시
$ python validator.py order_count.sql order_full_count.sql equals
=> 이 실행 방법을 DAG로 자동화 할 수 있다.
### 출력 결과 예시
```bash
result 1 = 15368
result 2 = 15368
Result of test: True
```
"""
import sys
import psycopg2
import configparser
import json
import requests

def connect_to_warehouse():
    parser = configparser.ConfigParser()
    parser.read("pipeline.conf")
    dbname = parser.get("aws_creds", "database")
    user = parser.get("aws_creds", "username")
    password = parser.get("aws_creds", "password")
    host = parser.get("aws_creds", "host")
    port = parser.get("aws_creds", "port")

    rs_conn = psycopg2.connect(
        "dbname=" + dbname,
        + " user=" + user,
        + " password=" + password,
        + " host=" + host,
        + " port=" + port
    )

    return rs_conn

def execute_test(
        db_conn,
        script_1,
        script_2,
        comp_operator
):
    """
    - 두 개의 스크립트로 구성된 테스트 실행
    - 비교 연산
    - 테스트 통과/실패에 대해 true/false 반환
    """

    # 첫번째 스크립트 실행하고 결과 저장
    try:
        cursor = db_conn.cursor()
        sql_file = open(script_1, 'r')
    except Exception as e:
        raise
    else:
        cursor.execute(sql_file.read())

        record = cursor.fetchone()
        result_1 = record[0]
        db_conn.commit()
    finally:
        cursor.close()
        sql_file.close()

    # 두번째 스크립트 실행하고 결과 저장
    try:
        cursor = db_conn.cursor()
        sql_file = open(script_2, 'r')
    except Exception as e:
        raise
    else:
        cursor.execute(sql_file.read())

        record = cursor.fetchone()
        result_2 = record[0]
        db_conn.commit()
    finally:
        cursor.close()
        sql_file.close()

    print(f"result 1 = {str(result_1)}")
    print(f"result 2 = {str(result_2)}")

    # comp_operator를 통해 값 비교
    match comp_operator:
        case "equals":
            return result_1 == result_2
        case "greater_equals":
            return result_1 >= result_2
        case "greater":
            return result_1 > result_2
        case "less_equals":
            return result_1 <= result_2
        case "less":
            return result_1 < result_2
        case "not_equal":
            return result_1 != result_2 # 값 비교

    return False

# 슬랙 메시지를 보내는 함수
def send_slack_notification(
        webhook_url,
        script_1,
        script_2,
        comp_operator,
        test_result
):
    try:
        if test_result == True:
            message = ("Validation Test Passed!: "
                       + script_1 + " / "
                       + script_2 + " / "
                       + comp_operator
                    )
        else:
            message = ("Validation Test Failed!: "
                        + script_1 + " / "
                        + script_2 + " / "
                        + comp_operator
                    )

        slack_data = {'text': message}
        response = requests.post(webhook_url,
                                 data = json.dumps(slack_data),
                                 headers = {
                                     'Content-Type': 'application/json'
                                 })
        if response.status_code != 200:
            print(response)
            return False
    except Exception as e:
        print("error sending slack notification")
        print(str(e))
        return False

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print("Usage: python validator.py"
            + "script.sql script2.sql "
            + "comparison_operator"
            )
        print("Valid comparison_operator values:")
        print("equals")
        print("greater_quals")
        print("greater")
        print("less_equals")
        print("less")
        print("not_equal")

        exit(0)

    if len(sys.argv) != 4:
        print("Usage: python validator.py"
            + "script1.sql script2.sql"
            + "comparsion_operator"
              )
        exit(-1)

    script_1 = sys.argv[1]
    script_2 = sys.argv[2]
    comp_operator = sys.argv[3]
    sev_level = sys.argv[4] # 심각도 수준에 따른 처리 추가

    # DWH에 연결
    db_conn = connect_to_warehouse()

    # 검증 테스트
    test_result = execute_test(
        db_conn,
        script_1,
        script_2,
        comp_operator
    )

    print(f"Result of test: {str(test_result)}")

    webhook_url = "http://localhost"

    if test_result == True:
        exit(0)
    else:
        send_slack_notification(
            webhook_url,
            script_1,
            script_2,
            comp_operator,
            test_result
        )
        exit(-1)
