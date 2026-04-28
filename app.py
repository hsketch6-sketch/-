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
           "맞춤법, 한글이외의 글자가 들어갔는지 5번 이상 확인해주고, 끝에 ?이 없다면 ?를 붙여."
            "이안에서만 추천해줘.제육볶음 2. 김치찌개 3. 된장찌개 4. 비빔밥 5. 불고기 6. 닭갈비 7. 부대찌개 8. 쌈밥 9. 육개장 10. 순두부찌개 11. 보쌈정식 12. 족발덮밥 13. 고등어구이 14. 갈치조림 15. 청국장 16. 돌솥비빔밥 17. 콩나물국밥 18. 돼지국밥 19. 순대국밥 20. 뼈해장국 21. 감자탕 22. 찜닭 23. 닭도리탕 24. 소불고기 25. 오징어볶음 26. 낙지덮밥 27. 게장백반 28. 떡갈비 29. 추어탕 30. 삼계탕 31. 갈비탕 32. 곰탕 33. 설렁탕 34. 수육국밥 35. 콩국수 36. 칼국수 37. 수제비 38. 잔치국수 39. 비빔국수 40. 묵밥2. 일식 & 에스닉 (깔끔한 한 끼)41. 돈카츠 42. 가츠동 43. 규동 44. 사케동(연어덮밥) 45. 초밥 46. 라멘 47. 우동(정식) 48. 소바 49. 텐동(튀김덮밥) 50. 커리라이스 51. 야키소바 52. 오코노미야키 53. 샤브샤브 54. 스키야키 55. 나베 56. 쌀국수 57. 분짜 58. 나시고랭 59. 팟타이 60. 푸팟퐁커리3. 중식 (강렬한 맛)61. 짜장면 62. 짬뽕 63. 볶음밥 64. 탕수육 65. 마라탕 66. 마라상궈 67. 꿔바로우 68. 유린기 69. 잡채밥 70. 마파두부 71. 울면 72. 간짜장 73. 군만두세트 74. 깐풍기 75. 고추잡채4. 양식 & 패스트푸드 (간편한 한 끼)76. 치즈버거 77. 불고기버거 78. 치킨버거 79. 페퍼로니 피자 80. 불고기 피자 81. 까르보나라 82. 토마토 파스타 83. 알리오올리오 84. 로제 파스타 85. 함박 스테이크 86. 돈가스 87. 치킨 샐러드 88. 샌드위치 89. 서브웨이 90. 퀘사디아 91. 타코 92. 브리또 93. 오므라이스 94. 필라프 95. 리조또5. 분식 및 기타 (익숙한 맛)96. 떡튀순(떡볶이 세트) 97. 치즈라면 98. 김밥 99. 쫄면 100. 스팸마요덮밥"

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
