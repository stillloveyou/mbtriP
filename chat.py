import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from llm import get_ai_response
import requests

# Set the page configuration
st.set_page_config(layout="wide", page_title="오직 P를 위해 J를 갈아넣은 여행 루트 짜기", page_icon="✈️")


# Display the title and caption
st.title("✈️ 오직 P를 위해 J를 갈아넣은 여행 루트 짜기")
st.caption(" 당신의 완벽한 여행을 위해 계획을 세워드립니다.")

def initialize_session_state():
    """Initialize session state variables."""
    if 'env_loaded' not in st.session_state:
        load_dotenv()
        st.session_state['env_loaded'] = True
    if 'message_list' not in st.session_state:
        st.session_state.message_list = []

def display_messages():
    """Display all previous messages."""
    for message in st.session_state.message_list:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def handle_user_input():
    """Handle new user input and generate AI response."""
    if user_question := st.chat_input(placeholder="궁금한 내용을 말씀해주세요!"):
        # Display the user's message
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.message_list.append({"role": "user", "content": user_question})

        # Generate and display AI response
        with st.spinner("답변을 생성하는 중입니다"):
            try:
                ai_response = get_ai_response(user_question)
                with st.chat_message("ai"):
                    st.write(ai_response)
                st.session_state.message_list.append({"role": "ai", "content": ai_response})
            except Exception as e:
                st.error(f"AI 응답 생성 중 오류가 발생했습니다: {e}")

def get_route(start, end):
    # 구글 맵 API 호출을 위한 함수
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&key={api_key}"
    response = requests.get(url)
    return response.json()

if user_question:
    # 간단한 키워드 매칭 예시
    if "경로" in user_question:
        start, end = user_question.split(" 경로 ")[1].split("에서")
        route_info = get_route(start.strip(), end.strip())
        # 여기서 route_info를 활용해 구글 맵에 경로를 표시

if user_question:
    if "경로" in user_question:
        start, end = user_question.split(" 경로 ")[1].split("에서")
        st.session_state['route'] = (start.strip(), end.strip())
        # 구글 맵 iframe URL 생성
        gmap_url = f"https://www.google.com/maps/dir/{start.strip()}/{end.strip()}/"
        components.iframe(gmap_url, height=500)

# 세션 상태 초기화
initialize_session_state()

# 페이지를 3:7 비율로 나누기
col1, col2 = st.columns([3, 7])

with col1:
    # 챗봇 인터페이스 표시
    st.sidebar.header("Private")
    user_question = st.sidebar.text_input("궁금한 내용을 말씀해주세요!")
    # 이전 메시지 모두 표시
    display_messages()
    # 새로운 사용자 입력 처리
    handle_user_input()

with col2:
    # 구글 맵 표시
    st.subheader("Google Maps")
    components.iframe("https://www.google.com/maps", height=500)