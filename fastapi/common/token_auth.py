import jwt
from datetime import datetime, timedelta
from typing import Dict

# 비밀 키와 알고리즘 설정
SECRET_KEY = "test1234dkagh1."
ALGORITHM = "HS256"

# JWT 생성 함수
def create_access_token(data: Dict[str, str], expires_delta: timedelta = timedelta(hours=1)) -> str:
    expiration = datetime.now() + expires_delta  # 토큰 유효기간 설정
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# JWT 생성 함수
def decode_access_token(token: str):
    try:
        print(type(token))
        if not isinstance(token, str):
            raise ValueError("Token must be a string.")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.exceptions.DecodeError:
        raise ValueError("Invalid token: Decoding failed.")
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")

if __name__ == "__main__":
    payload = jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0MTU3MDc4OX0.J94QhYiNWRZpJ96bS4jN97bhKDdqaoUgaAqgPA6HN1g", SECRET_KEY, algorithms=[ALGORITHM])
    print(payload)