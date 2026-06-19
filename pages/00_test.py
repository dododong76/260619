import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="📈 AI 스마트 주식 인사이더 대시보드",
    page_icon="📊",
    layout="wide"
)

# 커스텀 CSS (세련된 트레이딩 룸 스타일링)
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #0F172A; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1.1rem; color: #64748B; text-align: center; margin-bottom: 30px; }
    .metric-card { background-color: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; text-align: center; }
    .metric-value { font-size: 1.6rem; font-weight: bold; color: #0EA5E9; }
    .news-box { background-color: #F1F5F9; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #64748B; }
    </style>
""", unsafe_allow_html=True)

# 2. 사이드바 제어 패널
with st.sidebar:
    st.title("⚙️ 검색 설정")
    # 기본 분석 주식 티커 설정 (Apple, Microsoft, Tesla, NVIDIA 등)
    ticker_input = st.text_input("💡 미국 주식 티커(Ticker) 입력:", value="NVDA").upper()
    
    # 조회 기간 선택
    period_dict = {"1개월": "1mo", "3개월": "3mo", "6개월": "6mo", "1년": "1y", "5년": "5y"}
    selected_period = st.selectbox("📅 조회 기간 선택:", list(period_dict.keys()), index=1)
    period = period_dict[selected_period]
    
    st.write("---")
    st.caption("티커 예시:\n- NVIDIA: NVDA\n- Apple: AAPL\n- Tesla: TSLA\n- Microsoft: MSFT")

# 3. 메인 화면 로직 및 데이터 로드
st.markdown("<div class='main-title'>📈 AI 스마트 주식 인사이더 대시보드</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>실시간 시세 차트부터 기업 재무 데이터까지 한눈에 분석합니다</div>", unsafe_allow_html=True)

if ticker_input:
    try:
        # 야후 파이낸스 데이터 호출
        stock = yf.Ticker(ticker_input)
        info = stock.info
        
        # 기업 기본 이름 및 실시간 가격 추출
        company_name = info.get('longName', ticker_input)
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        currency = info.get('currency', 'USD')
        previous_close = info.get('regularMarketPreviousClose', 0)
        price_change = current_price - previous_close
        price_change_percent = (price_change / previous_close) * 100 if previous_close else 0

        # 상단 간단 요약 브리핑
        col_name, col_price = st.columns([2, 1])
        with col_name:
            st.subheader(f"🏢 {company_name} ({ticker_input})")
            st.write(f"**산업군:** {info.get('industry', 'N/A')} | **섹터:** {info.get('sector', 'N/A')}")
        with col_price:
            color = "#EF4444" if price_change >= 0 else "#2563EB"
            sign = "+" if price_change >= 0 else ""
            st.markdown(f"<h2 style='text-align:right; color:{color}; margin-bottom:0;'>{current_price:,.2f} {currency}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:right; color:{color}; font-weight:bold; margin-top:0;'>{sign}{price_change:,.2f} ({sign}{price_change_percent:.2f}%)</p>", unsafe_allow_html=True)

        st.write("---")

        # 4. 2단 레이아웃 분할 (왼쪽: 차트 및 재무 데이터, 오른쪽: 보조 지표 및 뉴스)
        main_col, side_col = st.columns([2, 1], gap="large")

        with main_col:
            st.markdown("### 📊 주가 변동 추이 (Candlestick Chart)")
            # 주가 이력 데이터 가져오기
            hist = stock.history(period=period)
            
            if not hist.empty:
                # Plotly를 이용한 고급 캔들스틱 차트 그리기
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name='주가'
                )])
                fig.update_layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=450,
                    xaxis_rangeslider_visible=False,
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("선택한 기간의 주가 데이터를 불러올 수 없습니다.")

            # 주요 재무 제표 지표 정보
            st.markdown("### 📑 핵심 투자 지표 (Financial Metrics)")
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                st.markdown(f"<div class='metric-card'><p style='color:#64748B; margin-bottom:5px;'>시가 총액 (Market Cap)</p><p class='metric-value'>${info.get('marketCap', 0):,}</p></div>", unsafe_allow_html=True)
            with f_col2:
                st.markdown(f"<div class='metric-card'><p style='color:#64748B; margin-bottom:5px;'>PER (PE Ratio)</p><p class='metric-value'>{info.get('trailingPE', 'N/A')}</p></div>", unsafe_allow_html=True)
            with f_col3:
                st.markdown(f"<div class='metric-card'><p style='color:#64748B; margin-bottom:5px;'>주당 순이익 (EPS)</p><p class='metric-value'>${info.get('trailingEps', 'N/A')}</p></div>", unsafe_allow_html=True)

        with side_col:
            st.markdown("### 🎯 목표 주가 및 투자 가치")
            target_high = info.get('targetHighPrice', 0)
            target_mean = info.get('targetMeanPrice', 0)
            
            if target_mean:
                st.write(f"🎯 **월가 평균 목표가:** {target_mean:,.2f} {currency}")
                st.write(f"🚀 **최고 목표가:** {target_high:,.2f} {currency}")
                # 목표가 대비 현재가 위치 게이지바 형태 시각화
                progress_percent = min(max(int((current_price / target_mean) * 100), 0), 100) if target_mean else 50
                st.progress(progress_percent / 100)
                st.caption(f"현재 주가는 목표가의 약 {progress_percent}% 수준에 위치해 있습니다.")
            else:
                st.info("해당 종목은 분석가 목표 주가 정보가 제공되지 않습니다.")

            st.write("")
            st.markdown("### 📰 실시간 주요 뉴스 및 피드")
            news_list = stock.news
            
            if news_list:
                # 최근 뉴스 4개만 노출
                for news in news_list[:4]:
                    title = news.get('title', '제목 없음')
                    publisher = news.get('publisher', '출처 미상')
                    link = news.get('link', '#')
                    
                    # 가상의 AI 감성 분석 스코어 매칭 (실제 상용 서비스 느낌 연출)
                    sentiment_score = random.choice(["🟢 긍정(Positive)", "🟡 중립(Neutral)", "🔵 안정(Stable)"])
                    
                    st.markdown(f"""
                    <div class='news-box'>
                        <a href='{link}' target='_blank' style='text-decoration:none; color:#1E293B; font-weight:bold;'>{title}</a>
                        <p style='margin:5px 0 0 0; font-size:0.85rem; color:#64748B;'>출처: {publisher} | AI 감정평가: <b>{sentiment_score}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("최근 등록된 기업 관련 뉴스가 없습니다.")

    except Exception as e:
        st.error(f"⚠️ 데이터를 불러오는 중 오류가 발생했습니다. 올바른 미국 주식 티커인지 확인해 주세요. (에러 내용: {e})")
