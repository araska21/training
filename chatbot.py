import streamlit as st
from openai import OpenAI

# Groq API 설정
client = OpenAI(
    api_key="",  # 🔐 Groq API 키
    base_url="https://api.groq.com/openai/v1"  # Groq API endpoint
)

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("💬 Groq 기반 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# 이모지 설정
user_emoji = "🧑 💻"
bot_emoji = "🤖"

# 이전 메시지 출력
for msg in st.session_state.messages[1:]:  # system 메시지는 생략
    with st.chat_message(msg["role"]):
        emoji = user_emoji if msg["role"] == "user" else bot_emoji
        # 이모지 앞뒤로 추가
        st.markdown(f"{emoji} **{msg['content']}** {emoji}")

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"{user_emoji} **{prompt}** {user_emoji}")

    # 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🤔 생각 중..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages,
                temperature=0.7
            )
            msg = response.choices[0].message.content
            st.markdown(f"{bot_emoji} **{msg}** {bot_emoji}")

    # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": msg})
