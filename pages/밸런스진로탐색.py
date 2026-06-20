import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="커리어 성향 테스트", page_icon="💼", layout="centered")

# =========================
# CSS (이미지 기반 맞춤형 커스텀 스타일)
# =========================
st.markdown("""
<style>
/* 기본 폰트 및 스타일 정리 */
h1, h2, h3, p {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    text-align: center;
}

/* 진행 상황 텍스트 */
.progress-text {
    font-size: 15px;
    color: #4a5568;
    font-weight: bold;
    text-align: left;
    margin-bottom: 5px;
}

/* 메인 타이틀 (🔥 당신의 업무 스타일은?) */
.main-title {
    font-size: 38px !important;
    font-weight: 800 !important;
    color: #2d3748;
    margin-top: 20px;
    margin-bottom: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
}

/* 서브 타이틀 (마음에 드는 하나의 선택지를...) */
.sub-title {
    font-size: 18px;
    color: #718096;
    margin-bottom: 40px;
}

/* 기본 버튼 공통 스타일 지우기 및 재정의 */
.stButton button {
    width: 100%;
    height: 65px;
    font-size: 20px !important;
    font-weight: bold !important;
    border-radius: 35px !important; /* 이미지처럼 둥글게 */
    border: none !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.2s ease-in-out;
}

/* 질문 화면의 좌측 버튼 (선택지 A - 연한 파랑 블록) */
div[data-testid="stHorizontalBlock"] > div:nth-of-type(1) .stButton button {
    background-color: #eef2ff !important;
    color: #3182ce !important;
    height: 180px !important; 
}
/* 👈 좌측 버튼 내부 글자 크기 강제 고정 */
div[data-testid="stHorizontalBlock"] > div:nth-of-type(1) .stButton button p {
    font-size: 50px !important; 
    font-weight: bold !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-of-type(1) .stButton button:hover {
    background-color: #ebf8ff !important;
    transform: scale(1.02);
}

/* 질문 화면의 우측 버튼 (선택지 B - 연한 노랑 블록) */
div[data-testid="stHorizontalBlock"] > div:nth-of-type(2) .stButton button {
    background-color: #fefcbf !important;
    color: #b7791f !important;
    height: 180px !important; 
}
/* 👈 우측 버튼 내부 글자 크기 강제 고정 */
div[data-testid="stHorizontalBlock"] > div:nth-of-type(2) .stButton button p {
    font-size: 50px !important; 
    font-weight: bold !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-of-type(2) .stButton button:hover {
    background-color: #fef08a !important;
    transform: scale(1.02);
}

/* 결과창 버튼은 기본 스타일 유지 */
.result-container .stButton button {
    background-color: #f7fafc !important;
    color: #4a5568 !important;
    border-radius: 12px !important;
    height: 50px;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 성향 및 질문 데이터
# =========================
traits = ["solo","team","creative","logic","help","freedom","stability","fun","challenge","speed"]

questions = [
    ("혼자 vs 팀", ("혼자 공부","solo"), ("팀 공부","team")),
    ("창의 vs 논리", ("창의","creative"), ("논리","logic")),
    ("안정 vs 도전", ("안정","stability"), ("도전","challenge")),
    ("자유 vs 규칙", ("자유","freedom"), ("규칙","stability")),
    ("재미 vs 효율", ("재미","fun"), ("효율","logic")),
    ("도움 vs 분석", ("도움","help"), ("분석","logic")),
    ("빠름 vs 정확", ("빠름","speed"), ("정확","logic")),
    ("혼자 작업 vs 협업", ("혼자","solo"), ("협업","team")),
]

job_profiles = {
    "소프트웨어 엔지니어": {"traits": ["logic", "solo"], "salary": "5000~12000만원", "difficulty": "⭐⭐⭐⭐☆", "desc": "논리 기반으로 시스템과 서비스를 개발하는 직업입니다."},
    "데이터 사이언티스트": {"traits": ["logic", "solo"], "salary": "6000~13000만원", "difficulty": "⭐⭐⭐⭐⭐", "desc": "데이터를 분석해 의사결정을 돕는 직업입니다."},
    "UX/UI 디자이너": {"traits": ["creative"], "salary": "4000~9000만원", "difficulty": "⭐⭐⭐☆☆", "desc": "사용자 경험을 설계하는 디자인 직업입니다."},
    "프로덕트 매니저": {"traits": ["team", "logic"], "salary": "6000~15000만원", "difficulty": "⭐⭐⭐⭐☆", "desc": "제품 방향과 팀을 조율하는 핵심 역할입니다."},
    "마케터": {"traits": ["creative", "team", "fun"], "salary": "3500~10000만원", "difficulty": "⭐⭐⭐☆☆", "desc": "브랜드와 제품을 시장에 알리는 직업입니다."},
    "창업가": {"traits": ["challenge", "freedom", "speed"], "salary": "변동 매우 큼", "difficulty": "⭐⭐⭐⭐⭐", "desc": "새로운 사업을 만들어 성장시키는 직업입니다."},
    "교사": {"traits": ["help", "stability", "team"], "salary": "3000~6000만원", "difficulty": "⭐⭐⭐⭐☆", "desc": "학생을 교육하고 성장시키는 직업입니다."},
    "상담사": {"traits": ["help", "team"], "salary": "3000~7000만원", "difficulty": "⭐⭐⭐⭐☆", "desc": "사람들의 심리와 문제를 돕는 직업입니다."},
}

# =========================
# 상태 초기화
# =========================
if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None

# 초기화 함수 정의
def reset_test():
    st.session_state.i = 0
    st.session_state.score = {}
    st.session_state.selected_job = None
    st.rerun()

# =========================
# 왼쪽 사이드바 메뉴 추가
# =========================
with st.sidebar:
    st.header("🧭 메뉴")
    st.write("언제든지 처음으로 돌아가거나 테스트를 다시 시작할 수 있습니다.")
    
    # 사이드바 버튼 스타일 조정을 위한 내부 마크다운 (선택사항)
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] .stButton button {
        height: 45px !important;
        font-size: 15px !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("🏠 메인으로 가기", key="sidebar_home_btn"):
        reset_test()
        
    if st.button("🔄 테스트 다시 하기", key="sidebar_reset_btn"):
        reset_test()

# =========================
# 기능 함수 (MBTI, 차트, 추천)
# =========================
def get_mbti(score):
    mbti_map = {"INTJ":["logic","solo"], "ENTP":["creative","challenge"], "INFP":["creative","freedom"], "ESTJ":["stability","team"]}
    best, best_score = None, 0
    for mbti, ts in mbti_map.items():
        s = sum(score.get(t,0) for t in ts)
        if s > best_score:
            best, best_score = mbti, s
    return best or "INFP"

def draw_radar(score):
    values = [score.get(t, 0) for t in traits]
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(traits), endpoint=False).tolist()
    angles += angles[:1]
    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2, color="#3182ce")
    ax.fill(angles, values, alpha=0.2, color="#3182ce")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(traits)
    st.pyplot(fig)

def recommend_jobs(score):
    results = []
    for job, info in job_profiles.items():
        match = sum(score.get(t, 0) for t in info["traits"])
        results.append((job, match))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]

# =========================
# 메인 화면 구현
# =========================
total_q = len(questions)

if st.session_state.i < total_q:
    # 1. 상단 진행도 표시 (이미지 싱크로)
    st.markdown(f"<p class='progress-text'>전체 {total_q}문제 중 {st.session_state.i + 1}번째 진행 중...</p>", unsafe_allow_html=True)
    st.progress((st.session_state.i + 1) / total_q)
    
    # 2. 중앙 타이틀 및 안내 문구
    st.markdown("<h1 class='main-title'>🔥 마음에 드는 하나를 선택하세요.</h1>", unsafe_allow_html=True)
    
    # 데이터 가져오기
    q = questions[st.session_state.i]
    
    # 3. 양방향 버튼 선택지 배치
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(q[1][0], key=f"btn_a_{st.session_state.i}"):
            st.session_state.score[q[1][1]] = st.session_state.score.get(q[1][1], 0) + 1
            st.session_state.i += 1
            st.rerun()
            
    with col2:
        if st.button(q[2][0], key=f"btn_b_{st.session_state.i}"):
            st.session_state.score[q[2][1]] = st.session_state.score.get(q[2][1], 0) + 1
            st.session_state.i += 1
            st.rerun()

# =========================
# 결과 화면
# =========================
else:
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    st.success("결과 분석 완료!")
    
    st.subheader("🧠 성향 분석")
    draw_radar(st.session_state.score)
    
    mbti = get_mbti(st.session_state.score)
    st.markdown(f"### 🎭 재미로 보는 MBTI: **{mbti}**")
    
    st.write("---")
    st.subheader("💼 추천 직업 TOP 5")
    top_jobs = recommend_jobs(st.session_state.score)
    
    for job, score in top_jobs:
        if st.button(f"{job} ({score}점 추천)", key=f"result_{job}"):
            st.session_state.selected_job = job
            
    if st.session_state.selected_job:
        job = st.session_state.selected_job
        info = job_profiles[job]
        
        st.markdown("---")
        st.markdown(f"### 📌 {job}")
        st.write(f"**🧠 설명:** {info['desc']}")
        st.write(f"**💰 연봉:** {info['salary']}")
        st.write(f"**📊 난이도:** {info['difficulty']}")
        st.write(f"**🔗 주요 성향:** {', '.join(info['traits'])}")
        
        if st.button("⬅ 뒤로가기", key="back_btn"):
            st.session_state.selected_job = None
            st.rerun()
            
    st.write("---")
    if st.button("🔄 테스트 다시 하기", key="reset_btn"):
        reset_test()
    st.markdown("</div>", unsafe_allow_html=True)