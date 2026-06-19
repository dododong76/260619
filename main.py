import streamlit as st

# 1. 페이지 기본 설정 및 스타일
st.set_page_config(
    page_title="진로 교육 MBTI 컬러셋 가이드",
    page_icon="🎨",
    layout="centered"
)

# 커스텀 CSS로 UI 가독성 높이기
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.1rem; color: #4B5563; text-align: center; margin-bottom: 30px; }
    .color-box { padding: 20px; border-radius: 10px; color: white; font-weight: bold; text-align: center; margin-bottom: 10px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
    .trait-badge { background-color: #F3F4F6; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem; color: #374151; display: inline-block; margin-right: 5px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# 2. MBTI별 진로 성향 및 컬러셋 데이터 구축
mbti_data = {
    "ISTJ": {
        "title": "청렴결백한 논리주의자",
        "desc": "철저하고 정확하며 신뢰성을 중시합니다. 명확한 규칙과 데이터 기반의 직무에 강합니다.",
        "careers": ["회계사", "금융 분석가", "경찰관", "공무원", "시스템 관리자"],
        "traits": ["체계적인", "신중한", "책임감 있는"],
        "colors": [
            {"name": "네이비 블루 (신뢰/정직)", "hex": "#1E3A8A"},
            {"name": "스틸 그레이 (논리/체계)", "hex": "#64748B"},
            {"name": "차콜 (안정감)", "hex": "#334155"}
        ]
    },
    "ISFJ": {
        "title": "용감한 수호자",
        "desc": "타인을 돕는 것에 보람을 느끼며 세심하고 따뜻합니다. 지원과 협력이 필요한 직무에 탁월합니다.",
        "careers": ["간호사", "사회복지사", "초등교사", "인사담당자(HR)", "상담가"],
        "traits": ["이타적인", "꼼꼼한", "헌신적인"],
        "colors": [
            {"name": "소프트 로즈 (따뜻함/배려)", "hex": "#FDA4AF"},
            {"name": "세이지 그린 (치유/안정)", "hex": "#86EFAC"},
            {"name": "스카이 블루 (평화)", "hex": "#93C5FD"}
        ]
    },
    "INFJ": {
        "title": "선의의 옹호자",
        "desc": "깊은 통찰력과 강한 인내심을 바탕으로 사람들에게 긍정적인 영감을 주는 일을 선호합니다.",
        "careers": ["심리상담사", "작가", "환경운동가", "인도주의 의사", "종교인"],
        "traits": ["통찰력 있는", "이상적인", "깊이 있는"],
        "colors": [
            {"name": "딥 퍼플 (영감/직관)", "hex": "#5B21B6"},
            {"name": "에메랄드 (치유/비전)", "hex": "#047857"},
            {"name": "미드나잇 블루 (깊은 사색)", "hex": "#1E1B4B"}
        ]
    },
    "INTJ": {
        "title": "용의주도한 전략가",
        "desc": "전략적 사고가 뛰어나며 시스템을 구축하고 거시적인 문제를 해결하는 데 능숙합니다.",
        "careers": ["소프트웨어 아키텍트", "경영 컨설턴트", "투자 분석가", "과학자", "전략 기획자"],
        "traits": ["전략적인", "독립적인", "분석적인"],
        "colors": [
            {"name": "옵시디언 블랙 (통제/전문성)", "hex": "#111827"},
            {"name": "일렉트릭 퍼플 (혁신)", "hex": "#7C3AED"},
            {"name": "다크 실버 (객관성)", "hex": "#9CA3AF"}
        ]
    },
    "ISTP": {
        "title": "만능 재주꾼",
        "desc": "상황 적응력이 뛰어나고 기계나 도구를 다루는 실질적인 문제 해결에 강합니다.",
        "careers": ["엔지니어", "데이터 분석가", "소방관", "파일럿", "소프트웨어 개발자"],
        "traits": ["실용적인", "관찰력 있는", "적응력 높은"],
        "colors": [
            {"name": "기어 그레이 (실용/기계)", "hex": "#4B5563"},
            {"name": "엠버 오렌지 (모험/순발력)", "hex": "#F59E0B"},
            {"name": "카키 그린 (현실주의)", "hex": "#78350F"}
        ]
    },
    "ISFP": {
        "title": "호기심 많은 예술가",
        "desc": "현재를 즐기며 감수성이 풍부합니다. 미적 감각을 발휘하거나 자율성이 보장되는 직무가 맞습니다.",
        "careers": ["디자이너", "화가/조각가", "조경가", "파티시에", "물리치료사"],
        "traits": ["예술적인", "자유로운", "온화한"],
        "colors": [
            {"name": "파스텔 라벤더 (감성/미적감각)", "hex": "#DDD6FE"},
            {"name": "살몬 핑크 (온화함)", "hex": "#FCA5A5"},
            {"name": "소프트 옐로우 (자유)", "hex": "#FEF08A"}
        ]
    },
    "INFP": {
        "title": "열정적인 중재자",
        "desc": "자신만의 가치관이 뚜렷하며, 사람들의 가능성을 열어주고 창의성을 발휘할 수 있는 일을 좋아합니다.",
        "careers": ["소설가/시인", "카운셀러", "예술 치료사", "인사(HR) 교육 전문가", "콘텐츠 크리에이터"],
        "traits": ["이상주의적인", "창의적인", "공감 능력이 뛰어난"],
        "colors": [
            {"name": "오키드 퍼플 (상상력/가치)", "hex": "#C084FC"},
            {"name": "포레스트 그린 (조화/평화)", "hex": "#15803D"},
            {"name": "로즈 골드 (인간애)", "hex": "#FB7185"}
        ]
    },
    "INTP": {
        "title": "논리적인 사색가",
        "desc": "이론과 분석에 강하며, 끊임없이 새로운 지식과 아이디어를 탐구하는 연구직에 적합합니다.",
        "careers": ["대학교수/연구원", "프로그래머", "철학자", "시스템 분석가", "수학자"],
        "traits": ["분석적인", "독창적인", "호기심 많은"],
        "colors": [
            {"name": "네온 사이언 (논리/디지털)", "hex": "#06B6D4"},
            {"name": "인디고 블루 (지적 탐구)", "hex": "#4338CA"},
            {"name": "슬레이트 바이올렛 (독창성)", "hex": "#6D28D9"}
        ]
    },
    "ESTP": {
        "title": "모험을 즐기는 사업가",
        "desc": "활동적이며 현실적인 문제를 즉각적으로 해결하는 능력이 탁월합니다. 역동적인 환경을 선호합니다.",
        "careers": ["영업 마케터", "기업가", "스포츠 감독", "경찰 간부", "펀드 매니저"],
        "traits": ["에너지 넘치는", "실전적인", "대담한"],
        "colors": [
            {"name": "파이어 레드 (에너지/대담함)", "hex": "#DC2626"},
            {"name": "선샤인 옐로우 (활동성)", "hex": "#FBBF24"},
            {"name": "탠저린 오렌지 (추진력)", "hex": "#EA580C"}
        ]
    },
    "ESFP": {
        "title": "자유로운 영혼의 연예인",
        "desc": "사교적이고 낙천적이며 주변 분위기를 밝게 만듭니다. 사람들과 소통하고 표현하는 직무에 어울립니다.",
        "careers": ["이벤트 플래너", "홍보 전문가(PR)", "연예인/배우", "승무원", "초등 교육가"],
        "traits": ["사교적인", "낙천적인", "표현력이 좋은"],
        "colors": [
            {"name": "핫 핑크 (스타성/사교성)", "hex": "#EC4899"},
            {"name": "비비드 오렌지 (즐거움)", "hex": "#FF7849"},
            {"name": "브라이트 옐로우 (에너지)", "hex": "#FFC82C"}
        ]
    },
    "ENFP": {
        "title": "재기발랄한 활동가",
        "desc": "창의적이고 에너지가 넘치며 활기찬 성향입니다. 새로운 아이디어를 제안하고 소통하는 기획 직무에 강합니다.",
        "careers": ["마케팅 기획자", "카피라이터", "이벤트 디렉터", "진로상담사", "저널리스트"],
        "traits": ["창의적인", "열정적인", "친화력 있는"],
        "colors": [
            {"name": "코랄 핑크 (열정/소통)", "hex": "#F43F5E"},
            {"name": "스카이 골드 (창의성/아이디어)", "hex": "#FCD34D"},
            {"name": "라임 그린 (활력)", "hex": "#84CC16"}
        ]
    },
    "ENTP": {
        "title": "뜨거운 논쟁을 즐기는 변론가",
        "desc": "두뇌 회전이 빠르고 독창적입니다. 기존의 틀을 깨고 새로운 돌파구를 찾는 벤처나 기획에 강합니다.",
        "careers": ["스타트업 창업가", "정치인", "전략 컨설턴트", "상품 기획자(MD)", "변호사"],
        "traits": ["도전적인", "혁신적인", "변론가적인"],
        "colors": [
            {"name": "마젠타 (혁신/도전)", "hex": "#D946EF"},
            {"name": "딥 사이언 (지적 스릴)", "hex": "#0891B2"},
            {"name": "오렌지 레드 (돌파력)", "hex": "#EF4444"}
        ]
    },
    "ESTJ": {
        "title": "엄격한 관리자",
        "desc": "조직적이고 실용적이며 규칙을 준수합니다. 목표를 달성하기 위해 사람과 상황을 관리하는 리더십 직무에 맞습니다.",
        "careers": ["프로젝트 매니저(PM)", "경영자", "군 장교", "공장 관리자", "호텔 지배인"],
        "traits": ["조직적인", "리더십 있는", "현실적인"],
        "colors": [
            {"name": "로얄 블루 (권위/체계)", "hex": "#1D4ED8"},
            {"name": "브릭 레드 (결단력/추진)", "hex": "#B91C1C"},
            {"name": "다크 그레이 (책임감)", "hex": "#374151"}
        ]
    },
    "ESFJ": {
        "title": "사교적인 외교관",
        "desc": "타인을 돕는 일에 열성적이며 커뮤니티의 조화를 중시합니다. 대면 서비스나 협동 중심의 직무에 최적입니다.",
        "careers": ["인사관리원", "초등/유치원 교사", "호스피탈리티 매니저", "홍보 담당자", "간호사"],
        "traits": ["협조적인", "친절한", "사교적인"],
        "colors": [
            {"name": "웜 코랄 (환대/친절)", "hex": "#FB923C"},
            {"name": "소프트 민트 (조화/안정)", "hex": "#2DD4BF"},
            {"name": "허니 옐로우 (협동심)", "hex": "#FBBF24"}
        ]
    },
    "ENFJ": {
        "title": "정의로운 천생 리더",
        "desc": "카리스마와 공감 능력을 겸비하여 타인을 올바른 방향으로 이끕니다. 교육 및 멘토링 직무에 빛을 발합니다.",
        "careers": ["교사/강사", "시민단체 리더", "인사담당 고위직", "정치인", "외교관"],
        "traits": ["지도력 있는", "이타적인", "공감하는"],
        "colors": [
            {"name": "골든 옐로우 (빛/리더십)", "hex": "#EAB308"},
            {"name": "딥 핑크 (인간애/포용)", "hex": "#DB2777"},
            {"name": "아쿠아 마린 (비전)", "hex": "#06B6D4"}
        ]
    },
    "ENTJ": {
        "title": "대담한 통솔자",
        "desc": "철저한 리더십과 목표 지향적 성향을 지녔습니다. 장기적인 비전을 제시하고 조직을 혁신하는 자리에 어울립니다.",
        "careers": ["CEO/기업가", "벤처 캐피탈리스트", "경영 컨설턴트", "정책 입안자", "변호사"],
        "traits": ["주도적인", "결단력 있는", "미래지향적인"],
        "colors": [
            {"name": "크림슨 레드 (결단력/열정)", "hex": "#991B1B"},
            {"name": "딥 네이비 (통솔력)", "hex": "#1E3A8A"},
            {"name": "차콜 블랙 (카리스마)", "hex": "#1F2937"}
        ]
    }
}

# 3. 화면 UI 렌더링
st.markdown("<div class='main-title'>🎨 진로 교육을 위한 MBTI 컬러셋 가이드</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>나의 MBTI 성향에 맞는 진로 색상과 직업군을 알아보세요!</div>", unsafe_allow_html=True)

# MBTI 선택 박스
mbti_list = list(mbti_data.keys())
selected_mbti = st.selectbox("🎯 본인의 MBTI를 선택하세요:", mbti_list)

if selected_mbti:
    data = mbti_data[selected_mbti]
    
    st.write("---")
    
    # 성향 타이틀 및 성향 배지
    st.subheader(f"✨ {selected_mbti} : {data['title']}")
    
    # 성향 키워드 배지 출력
    badge_html = "".join([f"<span class='trait-badge'>#{trait}</span> " for trait in data['traits']])
    st.markdown(badge_html, unsafe_allow_html=True)
    
    st.write(data['desc'])
    
    # 레이아웃 분할: 왼쪽(컬러셋), 오른쪽(추천 진로)
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🎨 대표 컬러셋")
        for color in data['colors']:
            st.markdown(
                f"<div class='color-box' style='background-color: {color['hex']};'>"
                f"{color['name']}<br><span style='font-size:0.8rem; font-weight:normal;'>{color['hex']}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )
            
    with col2:
        st.markdown("### 💼 추천 진로 및 직업")
        for career in data['careers']:
            st.markdown(f"- **{career}**")
            
        st.info(f"💡 **컬러 교육 활용 팁:**\n\n{selected_mbti} 학생들은 주로 위의 컬러들이 주는 심리적 안정감이나 에너지를 느낄 때 집중력이 높아집니다. 진로 포트폴리오나 공부방을 꾸밀 때 포인트 컬러로 활용해 보세요!")
