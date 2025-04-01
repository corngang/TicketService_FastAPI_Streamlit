import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import streamlit as st
import requests
import configparser
from common.validation import validate_useremail, validate_password

if st.session_state.logged_in == False:
    st.error("로그인하세요.")

config = configparser.ConfigParser()
config.read('/TicketService_FastAPI_Streamlit/streamlit_front/common/config.ini')

# URL 가져오기
# Fastapi login url
LOGIN_URL = os.getenv("LOGIN_URL", config['FASTAPI_URL']['LOGIN_URL'])

# 로그인 폼
st.title("로그인 페이지")

username = st.text_input("아이디")
password = st.text_input("비밀번호", type="password")

# 버튼 레이아웃 설정 (로그인 버튼과 회원가입 버튼을 옆에 배치)
if st.button("Login"):
    # 로그인 정보가 입력되었는지 확인
    if not username or not password:
        st.warning("아이디와 비밀번호를 입력해 주세요.")
    else:
        # 아이디 유효성 검사
        username_error = validate_useremail(username)
        if username_error:
            st.warning(username_error)
        else:
            # 비밀번호 유효성 검사
            password_error = validate_password(password)
            if password_error:
                st.warning(password_error)
            else:
                # FastAPI의 로그인 엔드포인트로 POST 요청
                data = {
                    "username": username,
                    "password": password
                }

                # POST 요청을 보내고 응답 받기
                response = requests.post(LOGIN_URL, json=data)

                if response.status_code == 200:
                    jwt_token = response.json().get("access_token")
                    st.success('로그인 성공')  # 로그인 성공
                    st.session_state["jwt_token"] = jwt_token
                    st.session_state.logged_in = True  # 로그인 상태 업데이트
                    st.rerun()
                elif response.status_code == 404:
                    st.error("존재하지 않는 아이디입니다.")
                elif response.status_code == 401:
                    st.error("비밀번호가 틀렸습니다.")
                else:
                    st.error(f"오류 발생: {response.status_code}")