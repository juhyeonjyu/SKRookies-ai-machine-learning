import streamlit as st
# 환경변수 가져올 때 사용
import os
# OpenAI API 호출
from openai import OpenAI
# .env 파일에 저장한 API 키 로드
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 메세지를 OpenAI에 보내기 위한 객체 생성
client = OpenAI(api_key=OPENAI_API_KEY)

st.title('Your friendly assistant, ChatGPT')

# st.session_state : 세션에 키-값 형식으로 데이터를 저장하는 변수
# 모델 지정
if 'openai_model' not in st.session_state :
    st.session_state.openai_model = 'gpt-4.1'

# 채팅 내용 저장 리스트
# 일종의 대화 히스토리 보관함 => 사용자별로 세션마다 유지되는 임시 저장 공간
if 'messages' not in st.session_state :
    st.session_state.messages = []

# 기존에 저장된 메세지가 있다면 출력
for msg in st.session_state.messages:
    with st.chat_message(msg['role']) :  # 블록으로 출력
        st.markdown(msg['content'])

# prompt => 사용자 입력 창
if prompt := st.chat_input('무엇을 도와드릴까요?') :
    st.session_state.messages.append({
        'role' : 'user',
        'content' : prompt
    })

    # 입력한 프롬프트 출력
    with st.chat_message('user') :
        st.markdown(prompt)

    # 모델에 전송 및 스트리밍 형식으로 출력
    with st.chat_message('assistant') :
        stream = client.chat.completions.create(
            model = st.session_state.openai_model,
            messages=[
                { 'role' : m['role'], 'content': m['content'] }     # m : st.session_state.messages 항목별로 꺼내기 위한 변수
                for m in st.session_state.messages
            ],
            stream = True
        )
        response = st.write_stream(stream)

    # 응답 저장
    st.session_state.messages.append(
        {
            'role' : 'assistant',
            'content' : response
        }
    )