import streamlit as st
from groq import Groq

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
                # Groq AI에게 질문 보내기 (Llama 3 모델 사용)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "너는 재치 있는 점심 메뉴 추천 전문가야. 입력이 헛소리면 쳐내고, 정상이면 메뉴 1개와 이유를 중학생처럼 재밌게 한 줄로 답해줘. 형식: [메뉴] 이유 그리고 반드시 한국어로 말해(글자 깨짐은 절때 안돼!) 그리고 ~~은 어때요? 같은 식으로해줘."
                        },
                        {
                            "role": "user",
                            "content": user_msg,
                        }
                    ],
                    model="llama-3.3-70b-versatile", # 고성능 무료 모델
                )
                
                result = chat_completion.choices[0].message.content
                st.success("✅ 오늘 너에게 딱 맞는 메뉴는?")
                st.subheader(result)
                st.balloons()
            except Exception as e:
                st.error(f"에러 발생: {e}")

# --- 4. 수익화 (후원 계좌) ---
st.markdown("---")
# 여기에 아까 만든 송금 링크 버튼 코드를 그대로 붙여넣으세요!

st.info("💡 **Tip**: 이 사이트가 맘에 드셨다면? 중1 개발자에게 사탕값을 후원해주세요!")

# 1. 후원 정보 설정 (본인 걸로 수정!)
my_bank = "토스"  # 예: 국민, 카카오, 신한 등
my_account = "100123063591" # 계좌번호 (숫자만)

# 2. 토스 송금 링크 생성
toss_link = f"https://toss.im{my_bank}&accountNo={my_account}"

# 3. 버튼 만들기
col1, col2 = st.columns(2) # 버튼을 예쁘게 배치하기 위해 칸 나누기

with col1:
    if st.button("💰 후원 계좌번호 보기"):
        st.success(f"{my_bank} {my_account}")

with col2:
    st.link_button("🎁 토스로 바로 송금", toss_link)

st.caption("여러분의 후원은 더 좋은 AI 서비스를 만드는 데 큰 힘이 됩니다!")
