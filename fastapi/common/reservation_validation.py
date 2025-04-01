from pydantic import BaseModel, Field, field_validator
# import re
# from datetime import date

# 데이터 모델 정의
class TicketInfo(BaseModel):
    ticket_id: int
    ticket_name: str
    ticket_description: str
    ticket_info: dict

class ReservationRequest(BaseModel):
    account_id: str
    ticket_name: str
    amount: int
    seat_level: str
    area_id: int

# class DuplicateCheckRequest(BaseModel):
#     name: str = Field(..., min_length=1, max_length=5)  # 이름 길이 1~5자
#     phone_number: str = Field(..., min_length=11, max_length=11)  # 전화번호는 11자 숫자
#     birth: str  # 생년월일 (날짜)

#     @field_validator("name")
#     @classmethod
#     def validate_name(cls, v):
#         if not re.match(r'^[가-힣]+$', v):  # 이름은 한글만 가능
#             raise ValueError("이름은 한글만 포함해야 합니다.")
#         return v

#     @field_validator("phone_number")
#     @classmethod
#     def validate_phone_number(cls, v):
#         if not v.isdigit() or len(v) != 11:  # 전화번호는 숫자 11자
#             raise ValueError("전화번호는 11자리 숫자만 가능합니다.")
#         return v

#     @field_validator("birth")
#     @classmethod
#     def validate_birth(cls, v):
#         # 생년월일 포맷 검사 (YYYY-MM-DD)
#         try:
#             birth_date = date.fromisoformat(v)
#         except ValueError:
#             raise ValueError("생년월일은 YYYY-MM-DD 형식이어야 합니다.")

#         # 생년월일이 1900.01.01부터 현재 날짜까지 선택 가능
#         if birth_date > date.today() or birth_date < date(1900, 1, 1):
#             raise ValueError("생년월일은 1900년 1월 1일부터 현재 날짜까지의 범위여야 합니다.")
        
#         return v