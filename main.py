import streamlit as st
import base64

# 1. 페이지 전체 설정 (가로로 넓고 시원하게 설정)
st.set_page_config(
    page_title="유퀴즈 테크&스포츠 포털",
    page_icon="🔮",
    layout="wide"
)

# --- 이미지의 세련된 감성을 담은 커스텀 CSS 적용 ---
st.markdown("""
    <style>
    /* 전체 배경 톤 조절 */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* 대형 상단 배너 디자인 변경 */
    .banner-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 10px 40px;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin-bottom: 45px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2);
    }
    
    /* 제공된 사진 스타일을 반영한 프리미엄 카드 컨테이너 */
    .premium-card {
        background-color: #ffffff;
        border: 2px solid #E2E8F0;
        border-radius: 24px; /* 둥근 모서리 강조 */
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        text-decoration: none !important;
        overflow: hidden;
        margin-bottom: 15px;
    }
    
    /* 마우스 오버 시 사진처럼 부드럽고 고급스럽게 뜨는 효과 */
    .premium-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08);
        border-color: #3B82F6; /* 테두리를 포인트 컬러로 변경 */
    }
    
    /* 카드 이미지 영역 */
    .card-img-wrapper {
        width: 100%;
        height: 220px;
        overflow: hidden;
        background-color: #F1F5F9;
    }
    .card-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    .premium-card:hover .card-img {
        transform: scale(1.05); /* 호버 시 이미지 살짝 확대 */
    }

    /* 카드 내부 텍스트 콘텐츠 (사진처럼 깔끔한 배치) */
    .card-content {
        padding: 28px;
        flex-grow: 1;
        background: #ffffff;
    }
    
    /* 지표 성격의 서브 뱃지 */
    .card-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 6px 14px;
        border-radius: 99px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 14px;
    }
    
    .card-title {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin-top: 0;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .card-text {
        font-size: 15px;
        color: #475569;
        line-height: 1.6;
    }
    
    /* 강조 텍스트 스타일 */
    .highlight-text {
        color: #1E3A8A;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 메인 화면 대형 배너
st.markdown("""
    <div class="banner-container">
        <h1 style="font-size: 46px; font-weight: 800; letter-spacing: -1px; margin-bottom: 14px;">🌟 진로탐색을 위한 밸런스 게임!</h1>
        <p style="font-size: 19px; opacity: 0.9; font-weight: 400;">밸런스 게임으로 진로탐색을 해보고, 머리 아플 땐 신나는 미니 게임도 즐겨보세요.</p>
    </div>
""", unsafe_allow_html=True)


# 3. 2단 레이아웃(컬럼)으로 메뉴 카드 배치
col1, col2 = st.columns(2)

# 이미지를 base64 형식으로 인코딩하여 HTML에 포함시키는 함수
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
            base64_image = base64.b64encode(data).decode()
        return f"data:image/png;base64,{base64_image}"
    except FileNotFoundError:
        # 이미지 파일이 없을 경우를 대비한 샘플 플레이스홀더
        return "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=600&auto=format&fit=crop"

# 이미지 바이너리 데이터 가져오기
balance_image = get_image_base64("밸런스게임.png")
soccer_image = get_image_base64("축구.png")


# --- 좌측 카드: 진로 탐색 밸런스 게임 ---
with col1:
    st.markdown(f"""
        <a href="pages/진로" target="_self" class="premium-card">
            <div class="card-img-wrapper">
                <img src="{balance_image}" class="card-img" alt="밸런스 게임">
            </div>
            <div class="card-content">
                <span class="card-badge">🎯 성향 분석 대시보드</span>
                <h2 class="card-title">🌋 1. 진로 밸런스 게임</h2>
                <p class="card-text">
                    단 5개의 기가 막힌 밸런스 질문을 통해 당신의 비즈니스 성향을 날카롭게 분석합니다!<br><br>
                    <span class="highlight-text">CEO, 개발자, 디자이너, PM, 데이터 사이언티스트</span> 중 젠슨 황과 가장 완벽한 케미를 자랑하는 당신의 천직을 확인해 보세요.
                </p>
            </div>
        </a>
    """, unsafe_allow_html=True)
    



# --- 우측 카드: 미니 축구 게임 ---
with col2:
    st.markdown(f"""
        <a href="pages/게임" target="_self" class="premium-card">
            <div class="card-img-wrapper">
                <img src="{soccer_image}" class="card-img" alt="축구 게임">
            </div>
            <div class="card-content">
                <span class="card-badge">⚽ 스트레스 해소 Zone</span>
                <h2 class="card-title">⚽ 2. 미니 축구 월드컵</h2>
                <p class="card-text">
                    머리 쓰는 진로 탐색에 지쳤다면? 짜릿한 스포츠 타임!<br><br>
                    간단하고 직관적인 컨트롤로 골문을 흔드는 <span class="highlight-text">실시간 미니 축구 게임</span>입니다. 친구와 함께 혹은 혼자서 최고 점수에 도전하고 스트레스를 날려버리세요!
                </p>
            </div>
        </a>
    """, unsafe_allow_html=True)
    


# 4. 하단 푸터 및 안내 문구
st.markdown("<br><br><hr style='border-color: #E2E8F0;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #94A3B8; font-size: 13px;'>© 2026 유퀴즈 온더 테크 대시보드 프로젝트. All rights reserved.</p>", 
    unsafe_allow_html=True
)