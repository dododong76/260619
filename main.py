import streamlit as st

# 1. 페이지 전체 설정 (가로로 넓고 시원하게 설정)
st.set_page_config(
    page_title="유퀴즈 테크&스포츠 포털",
    page_icon="🔮",
    layout="wide"
)

# 2. 메인 화면 대형 배너 (CSS를 활용해 세련된 그라데이션 배경 추가)
st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 40px; border-radius: 20px; text-align: center; color: white; margin-bottom: 30px;">
        <h1 style="font-size: 42px; margin-bottom: 10px;">🌟 진로탐색을 위한 밸런스 게임!</h1>
        <p style="font-size: 18px; opacity: 0.9;">밸런스 게임으로 진로탐색을 해보고 머리아프면 미니 게임도 즐겨보세요.</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# 3. 2단 레이아웃(컬럼)으로 메뉴 카드 배치
col1, col2 = st.columns(2)

# --- 좌측 카드: 진로 탐색 밸런스 게임 ---
with col1:
    # 카드 상단 데코레이션
    st.markdown("""
        <div style="background-color: #f0f7ff; border-left: 5px solid #2a5298; padding: 20px; border-radius: 0 15px 15px 0; min-height: 250px;">
            <h2 style="color: #1e3c72; margin-top: 0;">🌋 1. 진로 밸런스 게임</h2>
            <p style="color: #475569; font-size: 15px; line-height: 1.6;">
                단 5개의 기가 막힌 밸런스 질문을 통해 당신의 비즈니스 성향을 날카롭게 분석합니다!<br>
                <b>CEO, 개발자, 디자이너, PM, 데이터 사이언티스트</b> 중 젠슨 황과 가장 완벽한 케미를 자랑하는 당신의 천직을 확인해 보세요.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    # 💡 클릭 시 pages/진로.py 로 이동시키는 마법의 버튼
    if st.button("🚀 밸런스 게임 시작하기", use_container_width=True, type="primary"):
        st.switch_page("pages/진로.py")


# --- 우측 카드: 미니 축구 게임 ---
with col2:
    # 카드 상단 데코레이션
    st.markdown("""
        <div style="background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 20px; border-radius: 0 15px 15px 0; min-height: 250px;">
            <h2 style="color: #166534; margin-top: 0;">⚽ 2. 미니 축구 월드컵 게임</h2>
            <p style="color: #475569; font-size: 15px; line-height: 1.6;">
                머리 쓰는 진로 탐색에 지쳤다면? 짜릿한 스포츠 타임!<br>
                간단하고 직관적인 컨트롤로 골문을 흔드는 실시간 미니 축구 게임입니다. 친구와 함께 혹은 혼자서 최고 점수에 도전하고 스트레스를 날려버리세요!
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    # 💡 클릭 시 pages/게임.py 로 이동시키는 마법의 버튼
    if st.button("⚽ 축구 게임 입장하기", use_container_width=True):
        st.switch_page("pages/게임.py")


# 4. 하단 푸터 및 안내 문구
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #94a3b8; font-size: 13px;'>© 2026 유퀴즈 온더 테크 대시보드 프로젝트. All rights reserved.</p>", 
    unsafe_allow_html=True
)

    