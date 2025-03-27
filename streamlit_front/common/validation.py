import re

# # 아이디 유효성 검사 함수 -> 변경됨
# def validate_username(username):
#     if not username.isalnum():  # 영문과 숫자로만 이루어져야 함
#         return "아이디는 영문과 숫자로만 이루어져야 합니다."
#     if len(username) < 5 or len(username) > 20:
#         return "아이디는 5자 이상 20자 이하이어야 합니다."
#     return None

# 아이디 유효성 검사 함수 -> 변경됨
def validate_useremail(useremail):
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", useremail):
        return "이메일만 입력 가능합니다."
    return None

# 비밀번호 유효성 검사 함수
def validate_password(password):
    if len(password) < 8:
        return "비밀번호는 최소 8자 이상이어야 합니다."
    if not any(char.isdigit() for char in password):
        return "비밀번호는 최소 1개의 숫자를 포함해야 합니다."
    if not any(char.isalpha() for char in password):
        return "비밀번호는 최소 1개의 영문자를 포함해야 합니다."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "비밀번호는 최소 1개의 특수문자를 포함해야 합니다."
    if " " in password:
        return "비밀번호는 공백을 포함할 수 없습니다."
    return None

# 비밀번호 확인 유효성 검사
def validate_password_match(password, password_confirm):
    if password != password_confirm:
        return "비밀번호가 일치하지 않습니다."
    return None

def validate_name(name):
    if len(name) < 1 or len(name) > 5:
        return "이름은 1~5자 이내로 입력해주세요."
    if not re.match(r'^[가-힣]{1,5}$', name):
        return "이름은 한글만 가능합니다."
    return None

# 전화번호 유효성 검사 (11자리 숫자만)
def validate_phone_number(phone_number):
    if len(phone_number) != 11 or not phone_number.isdigit():
        return "전화번호는 11자리 숫자만 가능합니다."
    return None