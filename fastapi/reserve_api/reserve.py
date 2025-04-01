import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from common.reservation_validation import TicketInfo, ReservationRequest
from common.db_connect import select_query, insert_query
from common.token_auth import decode_access_token
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

import uvicorn

# 환경 변수로 호스트와 포트를 설정
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8003))


app = FastAPI()
# HTTPBearer 인스턴스 생성 (Bearer 토큰 사용)
security = HTTPBearer()


# 사용자 정의 예외 처리 함수
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# 인증을 위한 의존성
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials  # Bearer 토큰 가져오기
    user_info = decode_access_token(token)  # JWT 토큰 디코딩

    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return user_info  # 디코딩된 사용자 정보 반환


@app.post("/reserve/verify_user_info")
def verify_user_info(user_info: dict = Depends(get_current_user)):  # 이미 디코딩된 값을 받음
    account_id = user_info.get("sub")  # 토큰에서 가져온 id
    query = "SELECT name, phone_number, birth FROM account WHERE account_id = %s"
    user_data = select_query(query, (account_id,))

    if user_data:
        return {
            "name": user_data[0][0],
            "phone_number": user_data[0][1],
            "birth": user_data[0][2],
            "account_id": account_id
        }
    else:
        raise HTTPException(status_code=404, detail="Account not found")



@app.get("/reserve/ticket/{ticket_name}", response_model=TicketInfo)
def read_ticket_info(ticket_name: str):
    query = "SELECT ticket_id, description FROM ticket_info WHERE name = %s"
    ticket_data = select_query(query, (ticket_name,))

    if ticket_data is None: # 발생할 일이 없음
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_id, ticket_description = ticket_data[0]

    #  해당 티켓의 좌석별 가격, 총 좌석, 예약 좌석, 잔여 좌석
    # [('V', 300000, 5, 1, 4), ('R', 200000, 5, 0, 5), ('S', 150000, 5, 0, 5), ('A', 100000, 5, 0, 5)]
    query = """
        SELECT 
            ta.area_id,
            ta.level, 
            ta.price, 
            ta.max_amount,  
            CAST(COALESCE(SUM(r.amount), 0) AS SIGNED) AS reserved_amount,
            (ta.max_amount - CAST(COALESCE(SUM(r.amount), 0) AS SIGNED)) AS remaining_seats
        FROM ticket_area ta
        LEFT JOIN ticket_info ti ON ti.ticket_id = ta.ticket_id
        LEFT JOIN reserve r ON ta.area_id = r.area_id
        WHERE ta.ticket_id = %s
        GROUP BY ta.level, ta.price, ta.max_amount, ta.area_id;
    """
    result = select_query(query, (ticket_id,))

    # {'V': [1, 300000, 5, 5, 0], 'R': [2, 200000, 5, 0, 5], 'S': [3, 150000, 5, 0, 5], 'A': [4, 100000, 5, 0, 5]}
    # 순서대로 [area_id, price, max_amount, reserve_count, remaining_seats]
    ticket_info = {level: [area_id, price, max_amount, reserve_count,remaining_seats] for area_id, level, price, max_amount, reserve_count, remaining_seats in result}

    return TicketInfo(
        ticket_id=ticket_id,
        ticket_name=ticket_name,
        ticket_description=ticket_description,
        ticket_info = ticket_info
    )


# 예약 신청 API
@app.post("/reserve")
def reserve_ticket(request: ReservationRequest):

    query = """
        SELECT r.account_id, t.ticket_id, CAST(SUM(r.amount) AS SIGNED) AS total_reserved
        FROM reserve r
        JOIN ticket_area ta ON r.area_id = ta.area_id
        JOIN ticket_info t ON ta.ticket_id = t.ticket_id
        WHERE r.account_id = %s AND t.name = %s
        GROUP BY r.account_id, t.ticket_id;
    """
    result = select_query(query, (request.account_id, request.ticket_name))
    if result != []:
        print(result)
        print(request.amount)
        if int(result[0][2]) >=3 or int(result[0][2])+request.amount > 3:
            raise HTTPException(status_code=404, detail="3장까지 예매 가능합니다.")

    query = """
            INSERT INTO reserve (time, amount, is_deposit, account_id, area_id)
            VALUES (NOW(), %s, 0, %s, %s);
            """
    insert_query(query, (request.amount, request.account_id, request.area_id))
        
    return {"message": "예약이 완료되었습니다!"}

# python main.py에서 파일을 불러올 때 Uvicorn 서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
