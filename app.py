import streamlit as st
from groq import Groq
import re

# --- 1. Groq API 설정 ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# --- 2. 웹 페이지 설정 ---
st.set_page_config(page_title="AI 점심 추천기", page_icon="🍱")
st.title("🤖 중1 개발자의 '기분 분석' 점심 추천")
st.write("지금 기분과 못 먹는 음식을 알려주시면 AI가 완벽한 메뉴를 골라줍니다!")

# --- 3. 사용자 입력 섹션 ---
col1, col2 = st.columns(2) # 입력창 두 개를 나란히 배치

with col1:
    user_msg = st.text_input("지금 기분이나 상황", placeholder="예: 시험 망해서 우울해..")

with col2:
    exclude_food = st.text_input("못 먹는 음식/재료 (선택)", placeholder="예: 오이, 땅콩, 해산물")

if st.button("AI에게 추천받기"):
    if len(user_msg.strip()) < 2:
        st.warning("⚠️ 지금 기분을 조금만 더 자세히 적어줄래?")
    else:
        with st.spinner('AI가 최고의 메뉴를 고민 중...'):
            try:
                # 못 먹는 음식이 있을 경우 AI에게 줄 지침 추가
                exclude_instruction = ""
                if exclude_food.strip():
                    exclude_instruction = f"단, 반드시 **{exclude_food}**가 포함된 메뉴는 절대로 추천하지 마. 다른 메뉴로 골라줘."

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": f"너는 점심 메뉴 추천기야. 아래 규칙을 엄격히 지켜.\n"
                                       f"1. 형식: '메뉴이름 어때요?' 로만 답해.\n"
                                       f"2. 한글 이외의 글자는 절대 쓰지 말고 끝에 반드시 '?'를 붙여.\n"
                                       f"3. {exclude_instruction}\n"
                                       f"4. 식사와 관련 없는 질문엔 '다시 입력해주세요!'라고만 답해.\n"
                                       f"5. 반드시 아래 100개 메뉴 리스트 안에서만 골라:\n"
                                       f"제육볶음, 김치찌개, 된장찌개, 비빔밥, 불고기, 닭갈비, 부대찌개, 쌈밥, 육개장, 순두부찌개, 보쌈정식, 족발덮밥, 고등어구이, 갈치조림, 청국장, 돌솥비빔밥, 콩나물국밥, 돼지국밥, 순대국밥, 뼈해장국, 감자탕, 찜닭, 닭도리탕, 소불고기, 오징어볶음, 낙지덮밥, 게장백반, 떡갈비, 추어탕, 삼계탕, 갈비탕, 곰탕, 설렁탕, 수육국밥, 콩국수, 칼국수, 수제비, 잔치국수, 비빔국수, 묵밥, 돈카츠, 가츠동, 규동, 사케동, 초밥, 라멘, 우동정식, 소바, 텐동, 커리라이스, 야키소바, 오코노미야키, 샤브샤브, 스키야키, 나베, 쌀국수, 분짜, 나시고랭, 팟타이, 푸팟퐁커리, 짜장면, 짬뽕, 볶음밥, 탕수육, 마라탕, 마라상궈, 꿔바로우, 유린기, 잡채밥, 마파두부, 울면, 간짜장, 군만두세트, 깐풍기, 고추잡채, 치즈버거, 불고기버거, 치킨버거, 페퍼로니 피자, 불고기 피자, 까르보나라, 토마토 파스타, 알리오올리오, 로제 파스타, 함박 스테이크, 돈가스, 치킨 샐러드, 샌드위치, 서브웨이, 퀘사디아, 타코, 브리또, 오므라이스, 필라프, 리조또, 떡튀순, 치즈라면, 김밥, 쫄면, 스팸마요덮밥"
                        },
                        {
                            "role": "user",
                            "content": user_msg,
                        }
                    ],
                    model="llama-3.3-70b-versatile"
                )
                
                raw_result = chat_completion.choices[0].message.content
                # 한글, 숫자, 공백, ?, ! 제외하고 모두 삭제 (특수문자 및 외계어 방어)
                clean_result = re.sub(r'[^가-힣0-9\s?!]', '', raw_result).strip()

                if not clean_result: # 혹시라도 결과가 비어있을 경우 대비
                    st.error("😭 AI가 대답을 못 했어. 다시 한번 시도해볼래?")
                else:
                    st.success("✅ 오늘 너에게 딱 맞는 메뉴는?")
                    st.subheader(clean_result)
                    st.balloons()
                    
            except Exception as e:
                st.error(f"에러 발생: {e}")

# --- 4. 수익화 (후원 계좌) ---
st.markdown("---")
st.info("💡 **Tip**: 이 사이트가 맘에 드셨다면? 중1 개발자에게 사탕값을 후원해주세요!")

my_bank = "토스" 
my_account = "100123063591" 
toss_link = f"https://toss.im{my_bank}&accountNo={my_account}"

col_h1, col_h2 = st.columns(2)

with col_h1:
    if st.button("💰 후원 계좌번호 보기"):
        st.success(f"{my_bank} {my_account}")

with col_h2:
    st.link_button("🎁 토스로 바로 송금", toss_link)

st.caption("여러분의 후원은 더 좋은 AI 서비스를 만드는 데 큰 힘이 됩니다!")

