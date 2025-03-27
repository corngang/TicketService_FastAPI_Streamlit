import streamlit as st
from prometheus_client import start_http_server, Summary
import time

def logout():
    # if st.button("Log out"):
    st.session_state.logged_in = False
    st.rerun()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# print(st.session_state.page)

if st.session_state.logged_in:
    pg = st.navigation([
        st.Page("streamlit_main.py", title="Main"),
        st.Page(logout, title="Log out"),
        st.Page("streamlit_reserve.py", title="Reservation")
])

else:
    pg = st.navigation([
        st.Page("streamlit_main.py", title="Main"),
        st.Page("streamlit_login.py", title="Login"),
        st.Page("streamlit_user.py", title="Sign up"),
        st.Page("streamlit_reserve.py", title="Reservation")
    ])

pg.run()

# print(st.session_state.logged_in)
############ prometheus ###########
@st.cache_resource
def start_prometheus_server():
    start_http_server(8000)  # Prometheus metrics endpoint for frontend

# 처음에만 Prometheus 서버 시작
if "prometheus_started" not in st.session_state:
    st.session_state.prometheus_started = False

if not st.session_state.prometheus_started:
    start_prometheus_server()  # 서버가 아직 시작되지 않았다면 Prometheus 서버를 시작
    st.session_state.prometheus_started = True  # 서버 시작을 완료했음을 표시

############ prometheus ###########