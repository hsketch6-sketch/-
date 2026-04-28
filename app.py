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
                            "content": "너는 재치 있는 점심 메뉴 추천 전문가야. 입력이 헛소리거나 집가고 싶다등의 식사와 관련없으면 쳐내. 정상이면 메뉴 1개와 이유를 답해줘(단 너무 딱딱하지는 않게). 형식: [메뉴]추천드려요. \n 이유:[너가 그걸 추천하는 이유]. 한자, 일본어 없이 한국어만 사용해줘. 맞춤법을 3번 이상 검사하고 출력해줘!"
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
                clean_result = re.sub(r'[\u4e00-\u9fff]+', '', raw_result) # 한자 제거
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
