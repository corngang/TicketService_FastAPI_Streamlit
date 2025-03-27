import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI, HTTPException
from common.token_auth import create_access_token
from fastapi.responses import JSONResponse
from common.login_validation import LoginRequest
from common.db_connect import select_query
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import uvicorn

# 환경 변수로 호스트와 포트를 설정
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8001))

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
@app.post("/login")
async def login(request: LoginRequest):
    query = "SELECT * FROM account;"
    account_data = select_query(query)
    user_id_exists = False
    user_password = None
    # print(account_data)
    for row in account_data:
        # ID 존재 여부 확인
        if row[0] == request.username:
            user_id_exists = True
            user_password = row[2]
            break

    if  user_id_exists == False:
        raise HTTPException(status_code=404 , detail="존재하지 않는 아이디입니다.")
        
    # 비밀번호 검증
    
    if user_password != request.password:
        raise HTTPException(status_code=401, detail="비밀번호가 틀렸습니다.")
    
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



