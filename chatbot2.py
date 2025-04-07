import streamlit as st
from groq import Groq

# 페이지 설정을 가장 먼저 호출
st.set_page_config(page_title="AI 챗봇", page_icon="🤖")

# 사이드바 설정
with st.sidebar:
    st.header("🔑 Groq API 설정")
    api_key = st.text_input("API 키를 입력하세요:", type="password", 
                             help="Groq에서 발급받은 API 키를 입력해주세요.")
    
    # 모델 선택 드롭다운 추가
    model_options = [
        "llama3-8b-8192", 
        "mixtral-8x7b-32768", 
        "gemma-7b-it"
    ]
    selected_model = st.selectbox("사용할 모델을 선택하세요:", model_options)
    
    # API 키 검증 버튼
    if st.button("API 키 확인"):
        try:
            client = Groq(api_key=api_key)
            # 간단한 API 연결 테스트
            client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=selected_model
            )
            st.success("API 키가 성공적으로 연결되었습니다!")
        except Exception as e:
            st.error(f"API 키 연결 실패: {e}")

# Groq 클라이언트 초기화
client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        st.error(f"API 키 설정 중 오류 발생: {e}")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 챗봇 메인 로직
def main():
    st.title("Groq AI 챗봇")

    # 채팅 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if client and (prompt := st.chat_input("메시지를 입력하세요")):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Groq API 호출
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    model=selected_model,  # 사이드바에서 선택한 모델 사용
                    stream=True
                )
                
                # 스트리밍 응답 처리
                for chunk in chat_completion:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # AI 메시지 추가
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                st.error(f"응답 생성 중 오류 발생: {e}")

# 메인 함수 실행
if __name__ == "__main__":
    main()