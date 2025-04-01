import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import configparser
import streamlit as st
import requests
from datetime import datetime
from common.validation import validate_name, validate_phone_number, validate_useremail, validate_password, validate_password_match

# Config 읽기
config = configparser.ConfigParser()
config.read('/TicketService_FastAPI_Streamlit/streamlit_front/common/config.ini')

# URL 가져오기
USER_URL= os.getenv("USER_URL", config['FASTAPI_URL']['USER_URL'])

# 회원가입 페이지
st.title("회원가입 페이지")

# 입력 값
name = st.text_input("이름")
phone_number = st.text_input("전화번호")
birth = st.date_input("생년월일", min_value=datetime(1900,1,1), max_value=datetime.today())
username = st.text_input("아이디")
password = st.text_input("비밀번호", type="password")
password_confirm = st.text_input("비밀번호 확인", type="password")


# 가입 버튼
if st.button("회원가입"):
    # 입력 값 확인
    if username and password and password_confirm and name and phone_number and birth:
        # 이름 유효성 검사
        name_error = validate_name(name)
        if name_error:
            st.error(name_error)
        else:
            # 전화번호 유효성 검사
            phone_number_error = validate_phone_number(phone_number)
            if phone_number_error:
                st.error(phone_number_error)
            else:
                username_error = validate_useremail(username)
                if username_error:
                    st.warning(username_error)
                # 비밀번호 형식 및 일치 여부 검사
                else:
                    password_error = validate_password(password)
                    if password_error:
                        st.warning(password_error)
                    else:
                        password_match_error = validate_password_match(password, password_confirm)
                        if password_match_error:
                            st.error(password_match_error)
                        else:
                            # 가입 정보를 FastAPI 서버로 전송
                            url = USER_URL  # FastAPI 서버 URL (회원가입 엔드포인트)
                            data = {
                                "username": username,
                                "password": password,
                                "name": name,
                                "phone_number": phone_number,
                                "birth": birth.strftime("%Y-%m-%d")  # 생년월일 포맷팅
                            }

                            # POST 요청을 보내고 응답 받기
                            response = requests.post(url, json=data)

                            if response.status_code == 200:
                                st.success('회원가입 성공')  # 회원가입 성공 메시지
                                jwt_token = response.json().get("access_token")
                                st.session_state["jwt_token"] = jwt_token
                                # 로그인 페이지로 리다이렉션
                                st.session_state.logged_in = True  # 로그인 상태 업데이트
                                st.rerun()
                            elif response.status_code == 409:
                                st.error("이미 존재하는 아이디입니다.")
                            elif response.status_code == 410:
                                st.error("이미 가입된 사용자입니다.")
                            elif response.status_code == 411:
                                st.error("이미 존재하는 전화번호입니다.")
                            else:
                                st.error(f"오류 발생: {response.status_code}")
    else:
        st.warning("모든 필드를 입력해 주세요.")
