import streamlit as st
from groq import Groq
import re

# --- 1. Groq API 설정 ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# --- 2. 웹 페이지 설정 ---
st.set_page_config(page_title="AI 점심 추천기", page_icon="🍱")
st.title("🤖 중1 개발자의 '기분 분석' 점심 추천")
st.write("지금 기분이나 상황을 문장으로 적어주세요!")

# --- 3. 사용자 입력 섹션 ---
user_msg = st.text_input("입력창", placeholder="예: 오늘 시험 망해서 너무 우울해..")

if st.button("AI에게 추천받기"):
    if len(user_msg.strip()) < 5:
        st.warning("⚠️ 문장이 너무 짧아요!")
    else:
        with st.spinner('AI가 분석 중...'):
            try:
                # 모델을 현재 작동하는 llama-3.3-70b-versatile로 변경
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                           "content": "너는 점심 메뉴 추천기야. 다른 건 다 생략하고 딱 아래 형식으로만 답해줘. "
           "형식: 메뉴이름 어때요? "
           "주의: 대괄호[]나 특수문자를 절대 쓰지 말고 오직 한글로만 말해줘. "
           "예시: 제육볶음어때요?"
           "맞춤법, 한글이외의 글자가 들어갔는지 5번 이상 확인해줘!(?,!,.이 제대로 들어갔는지도 10번 확인해줘!)"

                        },
                        {
                            "role": "user",
                            "content": user_msg,
                        }
                    ],
                    model="llama-3.3-70b-versatile"
                )
                
                # 들여쓰기 수정 및 한자 제거 로직
                raw_result = chat_completion.choices[0].message.content
                clean_result = re.sub(r'[^가-힣0-9\s.,!?]', '', raw_result)
                clean_result = clean_result.replace(", ", " ").strip()
                st.success("✅ 오늘 너에게 딱 맞는 메뉴는?")
                st.subheader(clean_result) # 변수 이름 통일
                st.balloons()
            except Exception as e:
                st.error(f"에러 발생: {e}")

# --- 4. 수익화 (후원 계좌) ---
st.markdown("---")
st.info("💡 **Tip**: 이 사이트가 맘에 드셨다면? 중1 개발자에게 사탕값을 후원해주세요!")

my_bank = "토스" 
my_account = "100123063591" 

# 토스 공식 송금 링크 형식으로 수정
toss_link = f"https://toss.im{my_bank}&accountNo={my_account}"

col1, col2 = st.columns(2)

with col1:
    if st.button("💰 후원 계좌번호 보기"):
        st.success(f"{my_bank} {my_account}")

with col2:
    st.link_button("🎁 토스로 바로 송금", toss_link)

st.caption("여러분의 후원은 더 좋은 AI 서비스를 만드는 데 큰 힘이 됩니다!")
