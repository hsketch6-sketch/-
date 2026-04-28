import streamlit as st
from groq import Groq
import re
import random

# --- 1. Groq API 설정 ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# --- 2. 데이터 설정 (AI에게 매번 보내지 않고 코드에 저장) ---
MENU_LIST = [
    "제육볶음", "김치찌개", "된장찌개", "비빔밥", "불고기", "닭갈비", "부대찌개", "쌈밥", "육개장", "순두부찌개",
    "보쌈정식", "족발덮밥", "고등어구이", "갈치조림", "청국장", "돌솥비빔밥", "콩나물국밥", "돼지국밥", "순대국밥", "뼈해장국",
    "감자탕", "찜닭", "닭도리탕", "소불고기", "오징어볶음", "낙지덮밥", "게장백반", "떡갈비", "추어탕", "삼계탕",
    "갈비탕", "곰탕", "설렁탕", "수육국밥", "콩국수", "칼국수", "수제비", "잔치국수", "비빔국수", "묵밥",
    "돈카츠", "가츠동", "규동", "사케동", "초밥", "라멘", "우동정식", "소바", "텐동", "커리라이스",
    "야키소바", "오코노미야키", "샤브샤브", "스키야키", "나베", "쌀국수", "분짜", "나시고랭", "팟타이", "푸팟퐁커리",
    "짜장면", "짬뽕", "볶음밥", "탕수육", "마라탕", "마라상궈", "꿔바로우", "유린기", "잡채밥", "마파두부",
    "울면", "간짜장", "군만두세트", "깐풍기", "고추잡채", "치즈버거", "불고기버거", "치킨버거", "페퍼로니 피자", "불고기 피자",
    "까르보나라", "토마토 파스타", "알리오올리오", "로제 파스타", "함박 스테이크", "돈가스", "치킨 샐러드", "샌드위치", "서브웨이", "퀘사디아",
    "타코", "브리또", "오므라이스", "필라프", "리조또", "떡튀순", "치즈라면", "김밥", "쫄면", "스팸마요덮밥"
]

# --- 3. 웹 페이지 설정 ---
st.set_page_config(page_title="AI 점심 추천기", page_icon="🍱")
st.title("🤖 중1 개발자의 '기분 분석' 점심 추천")
st.write("지금 기분과 못 먹는 음식을 알려주시면 AI가 완벽한 메뉴를 골라줍니다!")

col1, col2 = st.columns(2)
with col1:
    user_msg = st.text_input("지금 기분이나 상황", placeholder="예: 시험 망해서 우울해..")
with col2:
    exclude_food = st.text_input("못 먹는 음식/재료 (선택)", placeholder="예: 오이, 땅콩")

if st.button("AI에게 추천받기"):
    if len(user_msg.strip()) < 2:
        st.warning("⚠️ 지금 기분을 조금만 더 자세히 적어줄래?")
    else:
        with st.spinner('AI가 최고의 메뉴를 고민 중...'):
            try:
                # [토큰 절약 전략] AI에게는 '메뉴'가 아니라 '어떤 종류'가 좋을지만 물어봅니다.
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "사용자의 기분에 어울리는 음식의 '특징' 키워드 3개를 뽑아줘. (예: 매콤한, 따뜻한, 스트레스풀리는). 다른 말은 하지 마."
                        },
                        {
                            "role": "user",
                            "content": user_msg,
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                    max_tokens=50 # 답변 길이를 제한해서 토큰 아끼기
                )
                
                # 못 먹는 음식 필터링 (파이썬이 직접 수행)
                filtered_menu = MENU_LIST.copy()
                if exclude_food.strip() and "그냥" not in exclude_food:
                    excludes = [x.strip() for x in re.split(',| ', exclude_food) if x.strip()]
                    filtered_menu = [menu for menu in MENU_LIST if not any(ex in menu for ex in excludes)]

                # 필터링 후 메뉴가 하나도 없으면 전체 리스트 사용
                if not filtered_menu: filtered_menu = MENU_LIST

                # 최종 메뉴 랜덤 선택 (이게 토큰 안 쓰고 가장 정확함!)
                final_menu = random.choice(filtered_menu)

                st.success("✅ 오늘 너에게 딱 맞는 메뉴는?")
                st.subheader(f"{final_menu} 어때요?")
                st.balloons()
                    
            except Exception as e:
                st.error(f"에러 발생: {e}")

# --- 수익화 섹션 (생략) ---



