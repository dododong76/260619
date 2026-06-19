import streamlit as st

# 1. 페이지 기본 설정 및 디자인 (가장 먼저 실행되어야 합니다)
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

# 2. 전역 MBTI 기반 퍼스널 컬러 데이터셋 구축 (오타 및 누락된 키 전면 수정)
mbti_data = {
    "ISTJ": {
        "title": "클래식 딥 네이비", "group": "🍁 가을 웜톤 (Deep Autumn)",
        "desc": "단정하고 신뢰감을 주는 클래식한 스타일이 가장 잘 어울립니다. 정돈되고 차분한 로우톤이 베스트입니다.",
        "tips": ["포멀한 비즈니스 룩", "무광 텍스처의 메이크업", "가죽 실버/골드 시계"], "traits": ["차분한", "클래식", "안정감있는"],
        "colors": [{"name": "네이비 블루", "hex": "#1E3A8A"}, {"name": "슬레이트 그레이", "hex": "#64748B"}, {"name": "딥 차콜", "hex": "#334155"}]
    },
    "ISFJ": {
        "title": "뮤티드 퓨어 로즈", "group": "🌸 여름 쿨톤 (Summer Mute)",
        "desc": "부드럽고 우아한 라벤더와 그레이시한 핑크가 자연스러운 생기를 더해줍니다. 과하지 않은 은은함이 매력입니다.",
        "tips": ["시폰/니트 소재의 데일리 룩", "로즈 브라운 계열의 음영", "실버 주얼리"], "traits": ["부드러운", "우아한", "자연스러운"],
        "colors": [{"name": "드라이 로즈", "hex": "#FDA4AF"}, {"name": "소프트 세이지", "hex": "#A7F3D0"}, {"name": "파스텔 스카이", "hex": "#BAE6FD"}]
    },
    "INFJ": {
        "title": "미스터리 이터널 퍼플", "group": "❄️ 겨울 쿨톤 (Winter Deep)",
        "desc": "깊이 있고 오묘한 분위기의 딥 퍼플과 미드나잇 컬러가 고혹적이고 지적인 무드를 연출해 줍니다.",
        "tips": ["벨벳/실크 광택 소재", "플럼/버건디 립 라이너", "화이트 골드 포인트"], "traits": ["오묘한", "신비로운", "지적인"],
        "colors": [{"name": "딥 플럼 퍼플", "hex": "#5B21B6"}, {"name": "에메랄드 그린", "hex": "#047857"}, {"name": "미드나잇 인디고", "hex": "#1E1B4B"}]
    },
    "INTJ": {
        "title": "시크 모던 옵시디언", "group": "❄️ 겨울 쿨톤 (Winter Dark)",
        "desc": "선명한 대비(Contrast)를 이룰 때 매력이 극대화됩니다. 블랙과 일렉트릭 컬러의 정석 배치가 가장 시크합니다.",
        "tips": ["모노톤 올블랙 룩", "선명한 풀 립(Full Lip)", "볼드한 실버 액세서리"], "traits": ["시크한", "도시적인", "카리스마"],
        "colors": [{"name": "옵시디언 블랙", "hex": "#111827"}, {"name": "일렉트릭 퍼플", "hex": "#7C3AED"}, {"name": "다크 실버", "hex": "#9CA3AF"}]
    },
    "ISTP": {
        "title": "얼반 아웃도어 카키", "group": "🍁 가을 웜톤 (Mute Autumn)",
        "desc": "꾸민 듯 안 꾸민 듯한 내추럴한 얼반 밀리터리 룩과 톤 다운된 웜 컬러가 도시적이고 자유로운 분위기를 줍니다.",
        "tips": ["레더/데님 매치", "매트하고 스모키한 브라운", "가죽 스트랩 소품"], "traits": ["내추럴", "와일드", "실용적인"],
        "colors": [{"name": "카키 브라운", "hex": "#4B5563"}, {"name": "엠버 골드", "hex": "#F59E0B"}, {"name": "딥 올리브", "hex": "#78350F"}]
    },
    "ISFP": {
        "title": "소프트 크림 라벤더", "group": "🌸 여름 쿨톤 (Summer Light)",
        "desc": "맑고 부드러운 파스텔 톤이 감수성 넘치는 예술가적 무드를 완성합니다. 탁하지 않고 투명한 컬러가 베스트입니다.",
        "tips": ["린넨/피치스킨 소재", "투명한 물광 메이크업", "내추럴 원석 주얼리"], "traits": ["감성적인", "소프트", "투명한"],
        "colors": [{"name": "미스티 라벤더", "hex": "#DDD6FE"}, {"name": "살몬 피치", "hex": "#FCA5A5"}, {"name": "크림 옐로우", "hex": "#FEF08A"}]
    },
    "INFP": {
        "title": "빈티지 오키드 포레스트", "group": "🍁 가을 / 🌸 여름 (Mute 믹스)",
        "desc": "몽환적이고 빈티지한 느낌을 주는 뮤트 톤의 조화가 독보적인 아우라를 만들어 냅니다.",
        "tips": ["에스닉/빈티지 레이어드 룩", "말린 장미(MLBB) 컬러링", "앤틱 원석 반지"], "traits": ["몽환적인", "빈티지", "유니크"],
        "colors": [{"name": "오키드 포그", "hex": "#C084FC"}, {"name": "올드 포레스트", "hex": "#15803D"}, {"name": "더스티 로즈", "hex": "#FB7185"}]
    },
    "INTP": {
        "title": "디지털 테크 사이언", "group": "❄️ 겨울 쿨톤 (Winter Bright)",
        "desc": "차가우면서도 눈에 띄는 네온 사이언과 인디고 블루가 지적이면서도 트렌디한 무드를 풍깁니다.",
        "tips": ["스트리트웨어 / 스포티 룩", "세미매트 피부 표현", "스마트 워치/실버 프레임"], "traits": ["테크니컬", "미래지향", "시원한"],
        "colors": [{"name": "네온 사이언", "hex": "#06B6D4"}, {"name": "인디고 헤더", "hex": "#4338CA"}, {"name": "바이올렛 일루전", "hex": "#6D28D9"}]
    },
    "ESTP": {
        "title": "스포티 파이어 레드", "group": "🌱 봄 브라이트 (Spring Bright)",
        "desc": "시선을 사로잡는 강렬한 원색과 채도 높은 컬러가 활력 넘치고 섹시한 이미지를 극대화해 줍니다.",
        "tips": ["에슬레저 룩 / 화려한 프린팅", "글로시하고 선명한 오렌지 레드립", "골드 체인"], "traits": ["에너제틱", "과감한", "비비드"],
        "colors": [{"name": "파이어 비비드 레드", "hex": "#DC2626"}, {"name": "네온 오렌지", "hex": "#EA580C"}, {"name": "선샤인 크롬 골드", "hex": "#FBBF24"}]
    },
    "ESFP": {
        "title": "팝핑 비비드 마젠타", "group": "🌱 봄 브라이트 (Spring Bright)",
        "desc": "인간 비타민 그 자체! 톡톡 튀는 팝 컬러와 화려한 글리터가 화사한 이목구비를 더욱 살려줍니다.",
        "tips": ["화려한 패턴 원피스", "트윙클 펄 글리터 메이크업", "유니크한 비즈 주얼리"], "traits": ["화려한", "톡톡튀는", "사교적인"],
        "colors": [{"name": "팝핑 핫 핑크", "hex": "#EC4899"}, {"name": "네온 만다린", "hex": "#FF7849"}, {"name": "브라이트 카나리아", "hex": "#FFC82C"}]
    },
    "ENFP": {
        "title": "스윗 코랄 라임", "group": "🌱 봄 웜톤 (Spring Light)",
        "desc": "밝고 통통 튀는 코랄과 라임 옐로우의 매칭이 특유의 사랑스럽고 발랄한 에너지를 돋보이게 합니다.",
        "tips": ["캐주얼 오버핏/파스텔 매치", "과즙 브라이트 코랄 메이크업", "아기자기한 패션 소품"], "traits": ["러블리", "발랄한", "비타민"],
        "colors": [{"name": "스윗 코랄", "hex": "#F43F5E"}, {"name": "네온 라임", "hex": "#84CC16"}, {"name": "소프트 파스텔 골드", "hex": "#FCD34D"}]
    },
    "ENTP": {
        "title": "네온 스파클 마젠타", "group": "❄️ 겨울 쿨톤 (Winter Bright)",
        "desc": "쉽게 소화하기 힘든 키치하고 강렬한 형광 마젠타나 테크니컬 사이언이 독창적인 개성을 200% 살려냅니다.",
        "tips": ["힙한 스트릿 패션/믹스매치", "컬러풀한 하이라이터", "아방가르드한 선글라스"], "traits": ["유니크", "트렌디", "키치한"],
        "colors": [{"name": "일렉트릭 마젠타", "hex": "#D946EF"}, {"name": "사이버 사이언", "hex": "#0891B2"}, {"name": "볼드 토마토 레드", "hex": "#EF4444"}]
    },
    "ESTJ": {
        "title": "파워풀 로얄 브릭", "group": "🍁 가을 웜톤 (Deep Autumn)",
        "desc": "무게감 있고 정갈한 로얄 블루와 브릭 레드가 카리스마 있는 정장이나 제복 핏 스타일을 완벽하게 받쳐줍니다.",
        "tips": ["테일러드 수트 / 칼정장", "매트한 딥 칠리 브릭 컬러", "고급스러운 골드 시계"], "traits": ["카리스마", "정갈한", "신뢰감"],
        "colors": [{"name": "로얄 네이비", "hex": "#1D4ED8"}, {"name": "딥 브릭 레드", "hex": "#B91C1C"}, {"name": "다크 세라믹 그레이", "hex": "#374151"}]
    },
    "ESFJ": {
        "title": "스윗 허니 코랄", "group": "🌱 봄 웜톤 (Spring Warm)",
        "desc": "누
