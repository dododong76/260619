import streamlit as st

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="🎨 나의 MBTI 기반 퍼스널 컬러 매칭 가이드",
    page_icon="🎨",
    layout="wide"
)

# 커스텀 CSS (UI 스타일링)
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #4C1D95; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.2rem; color: #4B5563; text-align: center; margin-bottom: 30px; }
    .color-box { padding: 25px; border-radius: 12px; color: white; font-weight: bold; text-align: center; margin-bottom: 15px; text-shadow: 1px 1px 3px rgba(0,0,0,0.6); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .trait-badge { background-color: #F5F3FF; padding: 6px 12px; border-radius: 20px; font-size: 0.95rem; color: #6D28D9; font-weight: bold; display: inline-block; margin-right: 6px; margin-bottom: 6px; }
    .intro-card { background-color: #FDF4FF; padding: 20px; border-radius: 10px; border-left: 5px solid #D946EF; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. 전역 MBTI 기반 퍼스널 컬러 데이터셋 구축
mbti_data = {
    "ISTJ": {
        "title": "클래식 딥 네이비", "group": "🍁 가을 웜톤 (Deep Autumn)",
        "desc": "단정하고 신뢰감을 주는 클래식한 스타일이 가장 잘 어울립니다. 정돈되고 차분한 로우톤이 베스트입니다.",
        "tips": ["포멀한 비즈니스 룩", "무광 텍스처의 메이크업", "가죽 실버/골드 시계"], "traits": ["차분한", "클래식", "안정감있는"],
        "colors": [{"name": "네이비 블루 (메인 수트 컬러)", "hex": "#1E3A8A"}, {"name": "슬레이트 그레이 (모던 베이스)", "hex": "#64748B"}, {"name": "딥 차콜 (무게감을 주는 포인트)", "hex": "#334155"}]
    },
    "ISFJ": {
        "title": "뮤티드 퓨어 로즈", "group": "🌸 여름 쿨톤 (Summer Mute)",
        "desc": "부드럽고 우아한 라벤더와 그레이시한 핑크가 자연스러운 생기를 더해줍니다. 과하지 않은 은은함이 매력입니다.",
        "tips": ["시폰/니트 소재의 데일리 룩", "로즈 브라운 계열의 음영", "실버 주얼리"], "traits": ["부드러운", "우아한", "자연스러운"],
        "colors": [{"name": "드라이 로즈 (생기 포인트)", "hex": "#FDA4AF"}, {"name": "소프트 사이지 (편안한 탑)", "hex": "#A7F3D0"}, {"name": "파스텔 스카이 (클린 베이스)", "hex": "#BAE6FD"}]
    },
    "INFJ": {
        "title": "미스터리 이터널 퍼플", "group": "❄️ 겨울 쿨톤 (Winter Deep)",
        "desc": "깊이 있고 오묘한 분위기의 딥 퍼플과 미드나잇 컬러가 고혹적이고 지적인 무드를 연출해 줍니다.",
        "tips": ["벨벳/실크 광택 소재", "플럼/버건디 립 라이너", "화이트 골드 포인트"], "traits": ["오묘한", "신비로운", "지적인"],
        "colors": [{"name": "딥 플럼 퍼플 (아이덴티티 코트)", "hex": "#5B21B6"}, {"name": "에메랄드 그린 (고급스런 스카프)", "hex": "#047857"}, {"name": "미드나잇 인디고 (슬림 아우터)", "hex": "#1E1B4B"}
        ]
    },
    "INTJ": {
        "title": "시크 모던 옵시디언", "group": "❄️ 겨울 쿨톤 (Winter Dark)",
        "desc": "선명한 대비(Contrast)를 이룰 때 매력이 극대화됩니다. 블랙과 일렉트릭 컬러의 정석 배치가 가장 시크합니다.",
        "tips": ["모노톤 올블랙 룩", "선명한 풀 립(Full Lip)", "볼드한 실버 액세서리"], "traits": ["시크한", "도시적인", "카리스마"],
        "colors":
