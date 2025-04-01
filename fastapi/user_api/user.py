import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from common.user_validation import UserRequest
from common.token_auth import create_access_token
from common.db_connect import select_query, insert_query
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import uvicorn

# 환경 변수로 호스트와 포트를 설정
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8002))

app = FastAPI()

# 사용자 정의 예외 처리 함수
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# 간단한 로그인 처리 예시
@app.post("/user")
def join_user(request: UserRequest):
    query = "SELECT * FROM account;"
    account_data = select_query(query)

    user_id_exists = False
    for row in account_data:
        # ID 존재 여부 확인
        if row[0] == request.username:
            user_id_exists = True
            break

    # 중복된 ID 확인
    if user_id_exists == True:
        raise HTTPException(status_code=409, detail="이미 존재하는 아이디입니다.")
    

    # 이름, 전화번호, 생년월일이 동일한 사용자가 있는지 확인
    for row in account_data:
        if row[1] == request.name and row[3] == request.phone_number and row[4] == request.birth:
            raise HTTPException(status_code=410, detail="이미 가입된 사용자입니다.")
        elif row[3] == request.phone_number:
            raise HTTPException(status_code=411, detail="이미 존재하는 전화번호입니다.")

    
    # 사용자 저장
    query = "INSERT INTO account (account_id, name, password, phone_number, birth) VALUES (%s, %s, %s, %s, %s)"
    parms = (request.username, request.name, request.password, f'+82{request.phone_number}', request.birth)
    insert_query(query, parms)

    # JWT 토큰 생성
    user_data = {"sub": request.username}
    access_token = create_access_token(user_data)

    # JSONResponse 객체 생성
    response_data = {"access_token": access_token}
    response = JSONResponse(content=response_data)
    
    # 쿠키에 토큰 저장
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="None", secure=True)
    
    return response
#python main.py에서 파일을 불러올 때 Uvicorn서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)