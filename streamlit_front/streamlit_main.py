import streamlit as st
from PIL import Image
from streamlit_image_select import image_select
import numpy as np
import os, time
from common.image_desc import ne1, iu, KimJaeJoong, Imhero
from prometheus_client import start_http_server, Summary
import time

# 이미지 파일 로딩을 캐시하기
@st.cache_resource
def load_image(image_path):
    return Image.open(image_path)


def stream_data(filename):
    file_dict = {"2NE1": ne1, "IU": iu, "KimJaeJoong": KimJaeJoong, "IMHero": Imhero}

    for word in file_dict[filename].split(" "):
        yield word + " "
        time.sleep(0.02)

# region image path 정보
abs_img_path = '/TicketService_FastAPI_Streamlit/streamlit_front/images'
image_list = os.listdir(f"{abs_img_path}/ticket")
image_list_path = sorted(os.path.join(f"{abs_img_path}/ticket", file_name) for file_name in image_list) # image list contain .jpg
ticket_list = sorted([i.split(".")[0] for i in image_list]) # no .jpg
top_img_path = f'{abs_img_path}/main/hao2.jpg'
# endregion

# region 이미지 크기 지정
image_width = 450  # 원하는 가로 크기
image_height = 600  # 원하는 세로 크기
# endregion

### token 값 확인
query_params = st.query_params
jwt_token = query_params.get("access_token", [None])[0]

# region 타이틀 설정 (타이틀 텍스트 설정)
st.set_page_config(page_title="HAO TICKET", page_icon="🎟️")
# 여백을 주기 위한 마크다운 수정
st.markdown('<style>div.block-container {padding-top: 3rem; padding-bottom: 1rem;}</style>', unsafe_allow_html=True)


# 두 개의 열로 나누기: 첫 번째 열은 이미지, 두 번째 열은 타이틀 텍스트
col1, col2 = st.columns([1, 4])  # 첫 번째 열은 좁고, 두 번째 열은 넓게

# 이미지 표시 (첫 번째 열에)
with col1:
    img = load_image(top_img_path)
    st.image(img, width=100)  # 이미지 크기를 100px로 설정

# 타이틀 텍스트 표시 (두 번째 열에, 이미지 중간에 맞추기)
with col2:
    st.markdown(
        f'<div style="display: flex; align-items: center; height: 100px; margin-left: -40px;">'  # 글씨를 더 왼쪽으로 이동
        f'<span style="font-size: 60px; white-space: nowrap; margin-top: 20px;">Welcome to HAO TICKET!</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
# endregion


# region "Select the Ticket", 예약 버튼
_, col4, _ = st.columns([2.3, 2, 1])
with col4:
    reserve_button = st.button("Reservation")  # 예약 버튼


    st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #000000;
        font-size: 30px;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        width: fit-content;
        margin-top: 20px;
        width: flex;
        height: 50px; /* 높이 통일 */
        display: flex;
        align-items: center; /* 세로 중앙 정렬 */
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    if reserve_button:
        # 예약 페이지로 리디렉션
        st.switch_page("streamlit_reserve.py")
    
# endregion


# region 이미지 선택 (4개의 이미지를 한 번에 표시)
img = image_select(
    label="",
    images=[
        load_image(image_list_path[0]),
        load_image(image_list_path[1]),
        load_image(image_list_path[2]),
        load_image(image_list_path[3]),
    ],
    captions=ticket_list
)
# print(img.filename)
filename = os.path.basename(img.filename).split(".")[0]
resized_img = img.resize((image_width, image_height))

# 이미지 선택 후 session_state에 저장
st.session_state.selected_image = filename  # 이미지 이름 저장

# 선택된 이미지에 따른 추가 동작
if isinstance(img, np.ndarray) or isinstance(img, Image.Image):
    # 이미지 표시 (이미지 클릭 시 해당 열에서 중앙 정렬)
    # st.image(img, width=image_width, use_container_width=True)
    col5, col6 = st.columns([1, 1]) 
    with col5:
        st.image(resized_img)
    with col6:
        # 버튼 클릭 시 스트리밍 시작
        if st.button(f"{filename} 티켓 정보"):
            st.write_stream(stream_data(filename))
# endregion
