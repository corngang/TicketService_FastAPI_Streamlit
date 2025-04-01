import mysql.connector
import configparser
import os

# config 파일에서 DB 정보 가져오기
def get_db_config():
    config = configparser.ConfigParser()
    config.read('/TicketService_FastAPI_Streamlit/fastapi/common/db.ini')

    # URL 가져오기
    IP = os.getenv("DB_IP", config['MYSQL']['IP'])
    PORT = os.getenv("DB_PORT", config['MYSQL']['PORT'])
    USER = os.getenv("DB_USER", config['MYSQL']['USER'])
    PASSWORD = os.getenv("DB_PASSWD", config['MYSQL']['PASSWORD'])
    DATABASE = os.getenv("DB_DATABASE", config['MYSQL']['DATABASE'])

    # DB 연결 설정 반환
    db_config = {
        'host': IP,
        'port': int(PORT),
        'user': USER,
        'password': PASSWORD,
        'database': DATABASE
    }
    return db_config

## DB 연결 함수
def connect_db():
    db_config = get_db_config()  # DB 설정 가져오기
    conn = mysql.connector.connect(**db_config)  # DB 연결
    return conn


# SELECT 쿼리 실행 함수
def select_query(query: str, data=None):
    conn = connect_db()  # DB 연결
    cursor = conn.cursor()  # 커서 생성
    result = None
    try:
        cursor.execute(query, data) if data else cursor.execute(query)
        result = cursor.fetchall()  # 결과 모두 가져오기
    except Exception as e:
        print(f"SELECT 쿼리 실행 중 오류 발생: {e}")
    finally:
        cursor.close()  # 커서 종료
        conn.close()  # 연결 종료
    return result


# INSERT 쿼리 실행 함수
def insert_query(query: str, data):
    conn = connect_db()  # DB 연결
    cursor = conn.cursor()  # 커서 생성
    try:
        cursor.execute(query, data)  # 데이터 바인딩 후 실행
        conn.commit()  # 변경 사항 커밋
        print(f"데이터가 {cursor.rowcount}개 삽입되었습니다.")
    except Exception as e:
        print(f"INSERT 쿼리 실행 중 오류 발생: {e}")
    finally:
        cursor.close()  # 커서 종료
        conn.close()  # 연결 종료


# UPDATE 쿼리 실행 함수
def update_query(query: str, data):
    conn = connect_db()  # DB 연결
    cursor = conn.cursor()  # 커서 생성
    try:
        cursor.execute(query, data)  # 데이터 바인딩 후 실행
        conn.commit()  # 변경 사항 커밋
        print(f"데이터가 {cursor.rowcount}개 업데이트되었습니다.")
    except Exception as e:
        print(f"UPDATE 쿼리 실행 중 오류 발생: {e}")
    finally:
        cursor.close()  # 커서 종료
        conn.close()  # 연결 종료


# DELETE 쿼리 실행 함수
def delete_query(query: str, data):
    conn = connect_db()  # DB 연결
    cursor = conn.cursor()  # 커서 생성
    try:
        cursor.execute(query, data)  # 데이터 바인딩 후 실행
        conn.commit()  # 변경 사항 커밋
        print(f"데이터가 {cursor.rowcount}개 삭제되었습니다.")
    except Exception as e:
        print(f"DELETE 쿼리 실행 중 오류 발생: {e}")
    finally:
        cursor.close()  # 커서 종료
        conn.close()  # 연결 종료


    # 사용 예시:
    # update_data('account', ['username', 'name'], ['newuser', '홍홍홍'], "username = 'testuser'")

# python main.py에서 파일을 불러올 때 Uvicorn 서버를 기동
if __name__ == "__main__":
    # query = "SELECT MAX(amount) FROM reserve WHERE ticket_id = %s"
    # reserved_amount = select_query(query, (1,))
    # print(reserved_amount)


    # query = "SELECT name, phone_number, birth FROM account WHERE account_id = %s"
    # user_data = select_query(query, ('testuser',))
    # print(user_data)



    query = """
                INSERT INTO reserve (time, amount, is_deposit, account_id, area_id)
                VALUES (NOW(), %s, 0, %s, %s);
                """
    insert_query(query, (2, 'testuser', 15))