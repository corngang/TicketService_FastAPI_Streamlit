from pydantic import BaseModel, Field, field_validator
import re
from datetime import date, datetime

class UserRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=50)  # ID 길이 제한 (5~50자)
    password: str = Field(..., min_length=8, max_length=30)  # 비밀번호 길이 제한 (8~30자)
    name: str = Field(..., min_length=1, max_length=5)  # 이름 길이 1~5자
    phone_number: str = Field(..., min_length=11, max_length=11)  # 전화번호는 11자 숫자
    birth: str  # 생년월일 (날짜)

    # 이메일 x
    # @field_validator("username")
    # @classmethod
    # def validate_username(cls, v):
    #     if not v.isalnum():  # 영문+숫자로만 이루어져야 함
    #         raise ValueError("ID는 영문과 숫자로만 이루어져야 합니다.")
    #     return v

    # 이메일 o
    @field_validator("username")
    @classmethod
    def validate_useremail(cls, v):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("이메일만 입력 가능합니다.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError("비밀번호는 최소 1개 이상의 숫자를 포함해야 합니다.")
        if not any(c.isalpha() for c in v):
            raise ValueError("비밀번호는 최소 1개 이상의 영문자를 포함해야 합니다.")
        if " " in v:
            raise ValueError("비밀번호는 공백을 포함할 수 없습니다.")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/|`~]', v):
            raise ValueError("비밀번호는 최소 1개 이상의 특수문자를 포함해야 합니다.")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not re.match(r'^[가-힣]+$', v):  # 이름은 한글만 가능
            raise ValueError("이름은 한글만 포함해야 합니다.")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if not v.isdigit() or len(v) != 11:  # 전화번호는 숫자 11자
            raise ValueError("전화번호는 11자리 숫자만 가능합니다.")
        return v

    @field_validator("birth")
    @classmethod
    def validate_birth(cls, v):
        v_date = datetime.strptime(v, "%Y-%m-%d").date()
        # 생년월일이 1900.01.01부터 현재 날짜까지만 선택 가능
        if v_date > date.today() or v_date < date(1900, 1, 1):
            raise ValueError("생년월일은 1900년 1월 1일부터 현재 날짜까지의 범위여야 합니다.")
        return v
