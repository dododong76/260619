import streamlit as st
import random

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="🤖 Hyper-AI 멀티에이전트 자산 가이드",
    page_icon="💰",
    layout="wide"
)

# 커스텀 CSS (세련되고 미래지향적인 다크/네온 UI 스타일링)
st.markdown("""
    <style>
    .main-title { font-size: 2.6rem; font-weight: bold; color: #1E1B4B; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.2rem; color: #4F46E5; text-align: center; margin-bottom: 30px; font-weight: 500; }
    .agent-card { background-color: #EEF2F6; padding: 18px; border-radius: 12px; border-top: 4px solid #4F46E5; margin-bottom: 15px; }
    .agent-title { font-weight: bold; color: #1E40AF; font-size: 1.1rem; margin-bottom: 5px; }
    .status-badge { background-color: #D1FAE5; color: #065F46; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; display: inline-block; }
    .result-box { background-color: #F8FAFC; padding: 25px; border-radius: 15px; border-left: 6px solid #10B981; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .mbti-tag { background-color: #EDE9FE; color: #6D28D9; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# 2. 고도화된 투자 및 소비 성향 데이터셋 (멀티에이전트 분석용)
finance_data = {
    "FWIS (플렉스형 미래주의자)": {
        "title": "트렌디한 얼리어답터형 자산가",
        "desc": "트렌디한 소비를 즐기면서도 테크, 스타트업, 해외 주식 등 미래 성장 가치가 높은 자산에 과감하게 투자하는 성향입니다.",
        "agent_psy": "현재의 행복과 미래의 성장 잠재력을 동시에 쫓는 균형 감각이 돋보입니다. 과소비만 통제하면 최고의 공격형 투자자가 될 수 있습니다.",
        "agent_fin": "자산의 60%를 미국 빅테크 및 혁신 기술 ETF에 배정하고, 20%는 현금성 자산, 20%는 트렌디한 대체투자(조각투자 등)를 추천합니다.",
        "portfolio": ["💻 미국 혁신 기술주 및 AI ETF (60%)", "🪙 유동성 현금 및 파킹통장 (20%)", "🎨 미술품/한정판 리셀 조각투자 (20%)"],
        "signals": "🚨 고위험 기술주 비중이 높으므로 시장 변동성 확대 시 분할 매수 전략 필수."
    },
    "SVRN (스마트 자본주의 수호자)": {
        "title": "철두철미한 데이터 기반 전략가",
        "desc": "불필요한 지출을 극도로 싫어하며, 철저한 예산 관리와 가성비 분석을 통해 안정적이고 확실한 자산 우상향을 추구합니다.",
        "agent_psy": "감정에 휘둘리지 않는 냉철한 소비 통제력이 강력한 무기입니다. 다만 지나친 방어 기전으로 좋은 투자 기회를 놓칠 수 있습니다.",
        "agent_fin": "안정적인 배당 성장주와 채권 ETF 위주의 세팅이 심리적 안정감을 줍니다. 절세 계좌(ISA, IRP)를 200% 활용하는 배색이 베스트입니다.",
        "portfolio": ["📈 고배당 주식 및 리츠(REITs) (50%)", "💵 국채 및 단기 금리형 ETF (30%)", "🥇 금(Gold) 및 원자재 자산 (20%)"],
        "signals": "🍏 세제 혜택 계좌 한도를 먼저 채우는 것이 수익률을 극대화하는 핵심 키포인트."
    },
    "CHIL (욜로 감성 아티스트)": {
        "title": "경험 중심의 라이프 해커",
        "desc": "물건을 소유하기보다 여행, 문화, 미식 등 '경험과 기억'에 자본을 투자합니다. 저축보다는 삶의 질 향상에 무게를 둡니다.",
        "agent_psy": "인생을 즐길 줄 아는 멋진 아티스트입니다. 하지만 소액 지출이 반복되어 자산 형성이 정체될 위험이 매우 큽니다.",
        "agent_fin": "강제 저축 시스템이 필수입니다. 소비할 때마다 자동으로 잔돈이 투자되는 '소액 자동 적립 펀드'나 '강제 적금 셋업'을 제안합니다.",
        "portfolio": ["🏦 자동이체 기반의 인덱스 펀드 (40%)", "✈️ 경험 자산 적립용 단기 특판 적금 (40%)", "📉 대형 우량주 적립식 매수 (20%)"],
        "signals": "⚠️ 가랑비에 옷 젖듯 나가는 구독 서비스와 자잘한 앱 결제 내역을 매달 1회 정기 검사하세요."
    }
}

# 3. 사이드바 네비게이션 생성
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&q=80&w=300", caption="Hyper AI Financial Network")
    st.title("🌐 AI 에이전트 허브")
    menu = st.radio(
        "메뉴를 선택해 주세요:",
        ["🏠 대시보드 안내", "🤖 AI 멀티에이전트 진단", "📊 2026 자산 트렌드 리포트"]
    )
    st.write("---")
    st.caption("가상의 AI 에이전트들이 협업하여 개인의 소비 성향과 거시 경제 트렌드를 융합 분석하는 시뮬레이션 공간입니다.")

# 4. 메뉴별 화면 렌더링
# -----------------------------------------------------
# 메뉴 1: 🏠 대시보드 안내
# -----------------------------------------------------
if menu == "🏠 대시보드 안내":
    st.markdown("<div class='main-title'>🤖 AI 멀티에이전트 자산 관리 가이드</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>단 한 명의 AI가 아닌, 각 분야 전문 에이전트들의 입체적 솔루션</div>", unsafe_allow_html=True)
    
    st.subheader("💡 멀티에이전트(Multi-Agent) 시스템이란?")
    st.write("심리 분석, 금융 공학, 트렌드 예측 등 **서로 다른 전문 지식을 가진 여러 개의 AI 에이전트들이 백엔드에서 토론을 거쳐** 사용자에게 최적의 정답을 도출해 내는 차세대 AI 구동 방식입니다.")
    
    st.markdown("""
    <div class='intro-card'>
        <h4>📌 시스템 이용 프로세스</h4>
        <ol>
            <li>사이드바에서 <b>🤖 AI 멀티에이전트 진단</b> 메뉴로 이동합니다.</li>
            <li>간단한 소비 및 지출 문답을 제출합니다.</li>
            <li><b>성향 분석 에이전트</b>와 <b>금융 자산 에이전트</b>가 실시간 시뮬레이션을 돌려 분석 결과를 연동합니다.</li>
            <li><b>📊 2026 자산 트렌드 리포트</b>에서 올 한 해 가장 뜨거운 거시 경제 키워드까지 마스터합니다.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("🎯 **오늘의 테크 트렌드:** 고정된 텍스트 가이드북에서 벗어나, 데이터와 AI 의견이 실시간으로 상호작용하는 다이내믹 포트폴리오 시스템을 경험해 보세요!")

# -----------------------------------------------------
# 메뉴 2: 🤖 AI 멀티에이전트 진단
# -----------------------------------------------------
elif menu == "🤖 AI 멀티에이전트 진단":
    st.markdown("<div class='main-title'>🤖 협업 AI 성향 분석 룸</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>AI 에이전트들이 실시간으로 당신의 데이터를 교차 분석합니다.</div>", unsafe_allow_html=True)
    
    # 가상 분석을 위한 질문 폼
    st.subheader("📝 나의 평소 금융 라이프스타일 체크")
    q1 = st.radio("1. 보너스나 여윳돈 100만 원이 생겼을 때 나의 행동은?", ["평소 사고 싶었던 위시리스트 제품을 바로 구매한다.", "일단 파킹통장이나 예적금에 넣어두고 지켜본다.", "전부터 눈여겨보던 주식이나 자산을 매수한다."])
    q2 = st.radio("2. 평소 지출에서 가장 큰 비용을 차지하는 항목은?", ["쇼핑, 가전제품, 최신 IT 기기 얼리어답팅", "식비, 생활비, 고정 저축 및 공과금", "여행, 문화생활, 소셜 모임 및 취미 활동"])
    
    st.write("")
    run_analysis = st.button("⚡ AI 에이전트 그룹에게 분석 요청하기")
    
    if run_analysis:
        st.write("---")
        st.subheader("🔄 에이전트 네트워크 가동 중...")
        
        # 문답 기반 성향 매칭 로직
        if "구매한다" in q1 and "쇼핑" in q2:
            mbti_key = "FWIS (플렉스형 미래주의자)"
        elif "넣어두고" in q1 or "식비" in q2:
            mbti_key = "SVRN (스마트 자본주의 수호자)"
        else:
            mbti_key = "CHIL (욜로 감성 아티스트)"
            
        data = finance_data[mbti_key]
        
        # 2단 레이아웃: 왼쪽은 일하는 AI 에이전트 브리핑, 오른쪽은 결과
        col1, col2 = st.columns([4, 5], gap="large")
        
        with col1:
            st.markdown("### 👥 담당 전문 AI 에이전트 라인업")
            
            st.markdown(f"""
            <div class='agent-card'>
                <div class='agent-title'>🧠 Agent_Psyche (소비 심리 전문가)</div>
                <div class='status-badge'>분석 완료</div>
                <p style='margin-top:8px; font-size:0.95rem; color:#374151;'>"{data['agent_psy']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='agent-card'>
                <div class='agent-title'>📈 Agent_Quant (금융 자산 공학자)</div>
                <div class='status-badge'>포트폴리오 빌드 완료</div>
                <p style='margin-top:8px; font-size:0.95rem; color:#374151;'>"{data['agent_fin']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("### 📊 종합 진단 리포트")
            st.markdown(f"""
            <div class='result-box'>
                <span class='mbti-tag'>{mbti_key}</span>
                <h4 style='margin-top: 15px; color:#1E1B4B;'>{data['title']}</h4>
                <p style='color:#4B5563; font-size:0.95rem;'>{data['desc']}</p>
                <hr style='margin:15px 0;'>
                <h5>🎯 에이전트 추천 최적 자산 배분 비율</h5>
            </div>
            """, unsafe_allow_html=True)
            
            # 추천 포트폴리오 목록 출력
            for item in data['portfolio']:
                st.markdown(f"✅ {item}")
                
            st.write("")
            st.info(data['signals'])

# -----------------------------------------------------
# 메뉴 3: 📊 2026 자산 트렌드 리포트
# -----------------------------------------------------
elif menu == "📊 2026 자산 트렌드 리포트":
    st.markdown("<div class='main-title'>📊 글로벌 자산 시장 핵심 메가트렌드</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>AI 에이전트 허브가 실시간 감시 중인 거시경제 키워드 아카이브</div>", unsafe_allow_html=True)
    
    st.write("변화무쌍한 거시 경제 속에서 내 자산을 지키기 위해 에이전트가 선정한 올해의 메인 금융 트렌드 4가지를 브리핑합니다.")
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("""
        <div style='background-color: #F0FDF4; padding: 20px; border-radius: 10px; margin-bottom:15px; border: 1px solid #BBF7D0;'>
            <h4 style='color: #166534;'>⚡ AI Infra & Semiconductor</h4>
            <p><b>현재 국면:</b> 슈퍼사이클 진입 및 고도화</p>
            <p><b>에이전트 브리핑:</b> 단순 소프트웨어 서비스를 넘어 전력망, 데이터센터 인프라 인프라, 차세대 칩 제조 밸류체인으로 자본이 쏠리는 현상이 뚜렷합니다.</p>
        </div>
        <div style='background-color: #F8FAFC; padding: 20px; border-radius: 10px; margin-bottom:15px; border: 1px solid #E2E8F0;'>
            <h4 style='color: #334155;'>🪙 디지털 자산 제도권 융합</h4>
            <p><b>현재 국면:</b> 글로벌 기관 자금 대거 유입</p>
            <p><b>에이전트 브리핑:</b> 주요 가상자산 현물 ETF 안착 이후, 기존 전통 자산(부동산, 채권)을 블록체인에 올리는 RWA(실물자산 토큰화) 시장이 급격히 팽창하고 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with g_col2:
        st.markdown("""
        <div style='background-color: #EFF6FF; padding: 20px; border-radius: 10px; margin-bottom:15px; border: 1px solid #BFDBFE;'>
            <h4 style='color: #1E40AF;'>🏦 금리 사이클 피벗(Pivot) 다변화</h4>
            <p><b>현재 국면:</b> 통화 정책 다각화 시기</p>
            <p><b>에이전트 브리핑:</b> 각국 중앙은행의 금리 인하 속도가 차별화됨에 따라 고금리 확정형 채권 자산과 통화 분산 투자(엔화, 달러 밸런싱)가 중요한 헤지 수단으로 부각됩니다.</p>
        </div>
        <div style='background-color: #FFF5F5; padding: 20px; border-radius: 10px; margin-bottom:15px; border: 1px solid #FEB2B2;'>
            <h4 style='color: #9B2C2C;'>🌿 기후 테크 및 ESG 2.0</h4>
            <p><b>현재 국면:</b> 글로벌 탄소 국경세 본격 규제화</p>
            <p><b>에이전트 브리핑:</b> 선언적 친환경을 넘어 실제 탄소 저감 능력을 증명하는 기업만이 글로벌 공급망에서 생존하며, 이는 곧 장기적 펀더멘탈의 척도가 됩니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.info("💡 **트렌드 결합 가이드:** 진단 페이지에서 도출된 나만의 포트폴리오 비율을 바탕으로, 위 메가트렌드 관련 메인 ETF(예: AI 인프라 관련 인덱스나 RWA 관련 핀테크 자산)를 매칭해 보면 가장 트렌디하고 견고한 투자 계획을 세울 수 있습니다.")
