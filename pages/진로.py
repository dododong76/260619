import streamlit as st
import time

# 1. 페이지 초기 설정 및 멋진 테마 구성
st.set_page_config(
    page_title="실리콘밸리 커리어 밸런스 게임",
    page_icon="🚀",
    layout="centered"
)

# 2. 게임에 사용할 5가지 핵심 밸런스 문제 정의
# 각 선택지(A, B)마다 어떤 직업 성향 점수(weights)를 올릴지 지정합니다.
QUESTIONS = [
    {
        "id": 1,
        "title": "🔥 당신의 업무 스타일은?",
        "choice_A": "세상을 바꿀 기가 막힌 아이디어를 기획하고 상상하기",
        "choice_B": "상상을 현실로 만드는 복잡하고 완벽한 시스템 구축하기",
        "weight_A": {"PM": 3, "Designer": 2, "CEO": 2},
        "weight_B": {"Developer": 4, "DataScientist": 3}
    },
    {
        "id": 2,
        "title": "🤝 젠슨 황과 베스트 프렌드가 된다면, 나누고 싶은 대화는?",
        "choice_A": "사람들의 마음을 사로잡는 비즈니스 네트워킹과 스토리텔링 전략",
        "choice_B": "엔비디아의 차세대 GPU 아키텍처와 딥러닝 연산 효율성",
        "weight_A": {"CEO": 4, "PM": 2, "Designer": 2},
        "weight_B": {"Developer": 3, "DataScientist": 4}
    },
    {
        "id": 3,
        "title": "🎨 제품을 만들 때 당신이 가장 중요하게 생각하는 요소는?",
        "choice_A": "사용자가 보자마자 감탄하는 아름답고 편리한 화면 인터페이스(UI/UX)",
        "choice_B": "수백만 명의 트래픽도 견뎌내는 굳건하고 안정적인 백엔드 서버 인프라",
        "weight_A": {"Designer": 5, "PM": 2},
        "weight_B": {"Developer": 5, "DataScientist": 2}
    },
    {
        "id": 4,
        "title": "📊 위기 상황! 프로젝트 방향성을 전면 수정해야 한다면?",
        "choice_A": "팀원들의 의견을 조율하고 전체적인 일정을 조율하는 오케스트라 지휘자",
        "choice_B": "현재 쌓여있는 수많은 실시간 데이터를 분석하여 실패 원인을 증명하는 탐정",
        "weight_A": {"PM": 4, "CEO": 3},
        "weight_B": {"DataScientist": 5, "Developer": 2}
    },
    {
        "id": 5,
        "title": "😎 유퀴즈에 출연한 당신! 대중에게 각인시키고 싶은 나의 매력은?",
        "choice_A": "트렌디한 가죽 재킷을 입고 유머러스하게 좌중을 압도하는 슈퍼 리더십",
        "choice_B": "조용하지만 묵묵히 세상을 바꾸는 기술을 증명해 내는 천재 엔지니어 포스",
        "weight_A": {"CEO": 5, "Designer": 2},
        "weight_B": {"Developer": 4, "DataScientist": 4}
    }
]

# 직업별 상세 설명 및 매칭 텍스트
JOB_DETAILS = {
    "CEO": {
        "title": "👑 실리콘밸리를 뒤흔들 '혁신적인 최고경영자(CEO)'",
        "desc": "당신은 젠슨 황처럼 확고한 비전과 강력한 카리스마, 그리고 대중을 사로잡는 스토리텔링 능력을 갖추고 있습니다. 위기 상황 속에서도 흔들리지 않고 팀을 이끌며, 기술과 비즈니스를 연결해 세상에 없던 가치를 창출하는 데 천부적인 재능이 있습니다.",
        "tip": "추천 도서: '나이키 창업자 필 나이트의 슈독', '스티브 잡스 자서전'"
    },
    "PM": {
        "title": "🎯 제품의 탄생을 지휘하는 '미다스의 손, 프로덕트 매니저(PM)'",
        "desc": "당신은 디자이너와 개발자, 그리고 경영진 사이에서 최고의 조율 능력을 발휘하는 소통의 달인입니다. 시장의 흐름을 읽는 눈이 탁월하며, 복잡한 문제를 단순하게 정의하여 유저가 진짜 원하는 제품을 기획하는 능력이 돋보입니다.",
        "tip": "추천 역량: 애자일(Agile) 스크럼 방법론, 유저 리서치"
    },
    "Developer": {
        "title": "💻 세상을 코드로 재창조하는 '무적의 소프트웨어 엔지니어'",
        "desc": "당신은 상상 속에만 존재하는 아이디어를 실제 구동 가능한 완벽한 프로그램으로 구현하는 디지털 아키텍트입니다. 논리적 사고력이 매우 뛰어나며, 복잡한 시스템 버그를 해결할 때 카타르시스를 느끼는 장인 정신을 가지고 있습니다.",
        "tip": "추천 분야: 클라우드 컴퓨팅(AWS), 시스템 아키텍처 설계"
    },
    "DataScientist": {
        "title": "🧬 숫자에 숨겨진 진실을 밝히는 '데이터 사이언티스트 / AI 연구원'",
        "desc": "당신은 겉으로 보기에 무작위해 보이는 거대한 데이터 속에서 핵심 인사이트와 패턴을 발견해 내는 데이터 탐정입니다. 통계적 사고와 인공지능 알고리즘을 활용해 기업의 미래 예측과 핵심 의사결정을 과학적으로 돕는 핵심 인재입니다.",
        "tip": "추천 분야: 머신러닝/딥러닝 LLM 모델링, 파이썬 기반 데이터 분석"
    },
    "Designer": {
        "title": "✨ 유저의 감성을 지배하는 '트렌디한 UI/UX 디자이너'",
        "desc": "당신은 세상을 아름답고 직관적으로 바라보는 예술가이자 문제 해결사입니다. 기술이 아무리 훌륭해도 유저가 사용하기 불편하면 의미가 없다고 믿으며, 픽셀 하나, 서체 하나에도 영혼을 담아 최상의 경험을 설계하는 능력이 뛰어납니다.",
        "tip": "추천 도서: '도널드 노먼의 디자인과 인간 심리'"
    }
}

# 3. 세션 상태(Session State) 초기화 (새로고침해도 게임 상태 유지)
if "stage" not in st.session_state:
    st.session_state.stage = "START"  # START, PLAYING, RESULT
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"CEO": 0, "PM": 0, "Developer": 0, "DataScientist": 0, "Designer": 0}

# 함수: 점수 반영 및 다음 문제 이동
def select_choice(weight_dict):
    for job, score in weight_dict.items():
        st.session_state.scores[job] += score
    
    if st.session_state.current_q < len(QUESTIONS) - 1:
        st.session_state.current_q += 1
    else:
        st.session_state.stage = "RESULT"

# 함수: 게임 초기화
def reset_game():
    st.session_state.stage = "START"
    st.session_state.current_q = 0
    st.session_state.scores = {"CEO": 0, "PM": 0, "Developer": 0, "DataScientist": 0, "Designer": 0}

# 4. 화면 렌더링 시작

# --- [시작 화면] ---
if st.session_state.stage == "START":
    st.markdown("<h1 style='text-align: center;'>🚀 실리콘밸리 커리어 밸런스 월드컵</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>유퀴즈 젠슨 황 편 스페셜 에디션</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=800&auto=format&fit=crop", caption="당신의 숨겨진 천직은 무엇일까요?")
    st.write("")
    
    st.info("💡 단 5개의 극단적인 밸런스 질문을 통해, 당신의 가치관과 업무 성향을 분석합니다. 마지막 순간 당신에게 어울리는 실리콘밸리 최고의 직업 리포트가 발급됩니다!")
    
    if st.button("🚀 나의 테크 커리어 찾기 시작하기", use_container_width=True, type="primary"):
        st.session_state.stage = "PLAYING"
        st.rerun()

# --- [게임 진행 화면] ---
elif st.session_state.stage == "PLAYING":
    q_idx = st.session_state.current_q
    current_question = QUESTIONS[q_idx]
    
    # 🎨 [추가] 버튼 글자 크기를 대폭 키우는 CSS 스타일링
    st.markdown("""
        <style>
        div.stButton > button p {
            font-size: 20px !important;
            font-weight: bold !important;
            line-height: 1.4 !important;
        }
        div.stButton > button {
            border-radius: 12px !important;
            padding: 15px !important;
            min-height: 100px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 상단 진행 바
    progress_percentage = (q_idx) / len(QUESTIONS)
    st.progress(progress_percentage, text=f"전체 5문제 중 {q_idx + 1}번째 진행 중...")
    
    st.write("")
    st.markdown(f"### {current_question['title']}")
    st.write("마음에 드는 하나의 선택지를 선택하세요.")
    st.write("")
    
    # 두 개의 거대한 선택지 버튼 배치 (2단 레이아웃)
    col1, col2 = st.columns(2)
    
    with col1:
        # 선택지 A 표시를 작고 귀엽게 변경
        st.markdown(
            "<span style='font-size: 13px; font-weight: bold; color: #1E3A8A; background-color: #DBEAFE; padding: 4px 10px; border-radius: 20px;'>선택지 A</span>", 
            unsafe_allow_html=True
        )
        st.write("") # 약간의 간격
        # 이제 이 버튼 안의 글자가 아주 크게 나옵니다!
        if st.button(current_question["choice_A"], key=f"A_{q_idx}", use_container_width=True):
            select_choice(current_question["weight_A"])
            st.rerun()
            
    with col2:
        # 선택지 B 표시를 작고 귀엽게 변경
        st.markdown(
            "<span style='font-size: 13px; font-weight: bold; color: #78350F; background-color: #FEF3C7; padding: 4px 10px; border-radius: 20px;'>선택지 B</span>", 
            unsafe_allow_html=True
        )
        st.write("") # 약간의 간격
        # 이제 이 버튼 안의 글자가 아주 크게 나옵니다!
        if st.button(current_question["choice_B"], key=f"B_{q_idx}", use_container_width=True):
            select_choice(current_question["weight_B"])
            st.rerun()

    # 하단에 이전으로 가기 혹은 리셋 버튼
    st.write("")
    st.write("")
    if st.button("↩️ 처음부터 다시 하기"):
        reset_game()
        st.rerun()