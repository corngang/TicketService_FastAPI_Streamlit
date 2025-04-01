import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import streamlit as st
import requests
import os
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('/TicketService_FastAPI_Streamlit/streamlit_front/common/config.ini')

# URL 가져오기
RESERVE_URL= os.getenv("RESERVE_URL", config['FASTAPI_URL']['RESERVE_URL'])
VERIFY_URL= os.getenv("VERIFY_URL", config['FASTAPI_URL']['VERIFY_URL'])
TICKET_INFO_URL= os.getenv("TICKET_INFO_URL", config['FASTAPI_URL']['TICKET_INFO_URL'])

#region 파일 리스트 및 이름
image_list = os.listdir("/TicketService_FastAPI_Streamlit/streamlit_front/images/ticket")
ticket_list = sorted([i.split(".")[0] for i in image_list])
#endregion

# region session 값 확인
if st.session_state.logged_in == False:
    st.switch_page("streamlit_login.py")

if "selected_image" not in st.session_state:
    st.session_state.selected_image = ticket_list[0]
# endregion

# page start
st.title("티켓 예약 시스템")

# 신청자 정보 입력
st.subheader("신청자 정보 입력")
jwt_token = st.session_state.get("jwt_token")
headers = {"Authorization": f"Bearer {jwt_token}"}

# 사용자 정보를 가져와서 기본 값으로 채워넣기

# 현재 로그인된 사용자 토큰 가져오기
response = requests.post(VERIFY_URL, headers=headers)
if response.status_code == 200:
    result = response.json()
    name = result["name"]
    phone_number = result["phone_number"]
    birth = result["birth"]
    account_id = result["account_id"]
    # 사용자가 정보를 수정할 수 없도록 비활성화
    st.text_input("이름", value=name, disabled=True)
    st.text_input("전화번호", value=phone_number, disabled=True)
    st.date_input("생년월일", value=datetime.strptime(birth, "%Y-%m-%d"), disabled=True)

else:
    st.error("정보를 불러오는 데 실패했습니다.")
    st.stop()

# 티켓 선택
st.subheader("티켓 선택")
ticket_choice = st.selectbox("티켓 선택", ticket_list, index=ticket_list.index(st.session_state.selected_image))
# st.image(ticket_options[ticket_choice], caption=ticket_choice, use_container_width=True)
response = requests.get(f'{TICKET_INFO_URL}/{ticket_choice}')
if response.status_code == 200:  
    result = response.json()
    ticket_id =  result["ticket_id"]
    ticket_info = result["ticket_info"]  # 순서대로 [area_id, price, max_amount, reserve_count, remaining_seats]

elif response.status_code == 404:
    st.error("정보를 불러오는 데 실패했습니다. 새로고침하여 재로그인해주세요.")
    st.stop()
else:
    st.error("정보를 불러오는 데 실패했습니다.")
    st.stop()

#region
# 세션 상태에 선택된 좌석 저장
if "selected_areas" not in st.session_state:
    st.session_state.selected_areas = 'no'

st.markdown("공연장 좌석 선택 시스템")
st.markdown(
    f'<div style="background-color: #000000; padding: 10px 10px; border-radius: 10px; text-align: center; color: white; font-size: 30px; font-weight: bold; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-left: auto; margin-right: auto; width: margin-top: 20px;">'
    f'STAGE'
    f'</div>',
    unsafe_allow_html=True,
)

# 버튼 스타일 지정 함수
def area_button(area_name, key_name, col):
    if col.button(area_name, key=key_name, use_container_width=True):
        st.session_state.selected_areas = key_name

# 첫 번째 줄 (R석 - VIP석 - R석)
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    area_button("R석", "R석_1", col1)
with col2:
    area_button("VIP석", "VIP석", col2)
with col3:
    area_button("R석", "R석_2", col3)

# 두 번째 줄 (S석 - R석 - S석)
col4, col5, col6 = st.columns([1, 3, 1])
with col4:
    area_button("S석", "S석_1", col4)
with col5:
    area_button("R석", "R석_3", col5)
with col6:
    area_button("S석", "S석_2", col6)

# 마지막 줄 (A석 - A석)
col7, _, _, col8 = st.columns([1, 2, 2, 1])
with col7:
    area_button("A석", "A석_1", col7)
with col8:
    area_button("A석", "A석_2", col8)
#endregion

# 선택된 영역 표시
st.subheader("선택된 구역")

# 좌석이 선택되지 않은 경우 버튼 비활성화
seat_selected = st.session_state.selected_areas != "no"


# 선택된 좌석 확인
selected_seat = st.session_state.selected_areas.split('_')[0] if '_' in st.session_state.selected_areas else st.session_state.selected_areas
# ticket_prices = {"VIP석": 300000, "R석": 200000, "S석": 150000, "A석": 100000}

col1,col2 = st.columns([1,1])
if seat_selected:
    remain_amount = ticket_info[selected_seat[0]][-1]
else:
    remain_amount = 0

with col1:
    if seat_selected:
        st.markdown(f"{selected_seat} 구역은 {remain_amount}좌석 남았습니다.  \n티켓 당 최대 3매까지 구매 가능합니다.(계정별로 적용)")
    else:
        st.markdown("선택된 구역이 없습니다.")

with col2:
    if seat_selected:
        if remain_amount > 3:
            remain_amount = 3
        elif remain_amount == 0:
            st.warning("매진입니다. 예약할 수 없습니다.")
            st.stop()
        # 인원 선택 부분
        num_people = st.number_input(
            "인원 선택",
            min_value=1,
            max_value=remain_amount,
            step=1,
            disabled=not seat_selected,  # 좌석이 선택되지 않으면 비활성화
            label_visibility="collapsed"  # 라벨 숨기기
        )

# 가격 계산
total_price = ticket_info[selected_seat[0]][1] * num_people if seat_selected else 0

# 가격을 `st.metric`으로 강조
if seat_selected:
    st.metric("총 가격", f"{total_price:,}원", delta=None)


# 예약 신청 버튼
if st.button("예약 신청", disabled=not seat_selected):  # 좌석이 선택되지 않으면 비활성화
    # print(type(account_id), type(ticket_choice), type(num_people), type(selected_seat[0]), type(ticket_info[selected_seat[0]][0]))
    reservation_data = {
        "account_id": account_id,
        "ticket_name": ticket_choice,
        "amount": num_people,
        "seat_level": selected_seat[0],
        "area_id": ticket_info[selected_seat[0]][0]
    }
    response = requests.post(RESERVE_URL, json=reservation_data)
    if response.status_code == 200:
        st.success("예약이 신청되었습니다!")
    elif response.status_code == 404:
        st.error(f"티켓 당 3장까지 예매 가능합니다. {ticket_choice} 티켓은 이미 예매하신 이력이 있습니다.")
    else:
        st.error("예약 신청 실패. 다시 시도해주세요.")