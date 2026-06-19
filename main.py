import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. 페이지 기본 설정 (무조건 가장 첫 줄에 실행되어야 합니다)
st.set_page_config(
    page_title="🌍 120년 기후 트렌드 인사이더",
    page_icon="🌡️",
    layout="wide"
)

# 2. 기상청 CSV 데이터 맞춤형 로드 로직
csv_url = "https://raw.githubusercontent.com/dododong76/260619/main/ta_20260619190504.csv"

try:
    # 기상청 데이터의 한글 깨짐(cp949) 및 상단 빈 줄/안내문 제거(skiprows=7) 반영
    df = pd.read_csv(csv_url, encoding='cp949', skiprows=7)
    
    # 깃허브 원본 컬럼명 양 끝의 미세한 공백 제거
    df.columns = df.columns.str.strip()
    
    # '날짜' 열을 파이썬 날짜 데이터로 안전하게 변환
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['연도'] = df['날짜'].dt.year

    # 3. 메인 화면 타이틀 및 디자인
    st.markdown("""
        <div style='text-align:center; padding: 10px;'>
            <h1 style='color: #DC2626;'>🌍 지구온난화 타임머신</h1>
            <p style='color: #4B5563; font-size: 1.1rem;'>1907년부터 2026년까지의 역사적 기온 데이터 트렌드 분석</p>
        </div>
        <hr style='margin-top:0;'>
    """, unsafe_allow_html=True)

    # 4. 상단 요약 지표 (KPI 메트릭) 계산
    start_year = int(df['연도'].min())
    end_year = int(df['연도'].max())
    
    # 과거 10년 vs 최근 10년 평균 기온 비교
    past_avg = df[df['연도'] < (start_year + 10)]['평균기온(℃)'].mean()
    recent_avg = df[df['연도'] > (end_year - 10)]['평균기온(℃)'].mean()
    temp_rise = recent_avg - past_avg

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="📊 데이터 관측 시작", value=f"{start_year}년")
    with m_col2:
        st.metric(label="📅 최근 업데이트 연도", value=f"{end_year}년")
    with m_col3:
        st.metric(label="🔥 약 120년간 평균 기온 상승", value=f"{temp_rise:.2f} °C", delta=f"{temp_rise:.2f} °C", delta_color="inverse")

    st.write("")

    # 5. 연도별 평균 기온 데이터 그룹화 (컬럼명 특수문자 대응 완료)
    yearly_summary = df.groupby('연도')['평균기온(℃)'].mean().reset_index()

    # 6. Plotly 선 그래프 시각화
    st.subheader("📈 연도별 평균 기온 추이 선 그래프")
    
    fig = go.Figure()
    
    # 메인 변동 선
    fig.add_trace(go.Scatter(
        x=yearly_summary['연도'],
        y=yearly_summary['평균기온(℃)'],
        mode='lines+markers',
        name='연평균 기온',
        line=dict(color='#EF4444', width=2.5),
        marker=dict(size=4),
        hovertemplate='<b>%{x}년</b><br>평균 기온: %{y:.2f}°C<extra></extra>'
    ))
    
    # 장기 우상향 추세선 계산
    z = np.polyfit(yearly_summary['연도'], yearly_summary['평균기온(℃)'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=yearly_summary['연도'],
        y=p(yearly_summary['연도']),
        mode='lines',
        name='장기 상승 추세선',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))

    fig.update_layout(
        xaxis_title="연도 (Year)",
        yaxis_title="평균 기온 (°C)",
        hovermode="x unified",
        template="plotly_white",
        height=500,
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **그래프 활용 팁:** 마우스를 그래프 선 위에 올리면 해당 연도의 정확한 평균 기온을 실시간으로 확인할 수 있습니다.")

except Exception as e:
    st.error(f"⚠️ 데이터를 읽어오는 중 분석 엔진에 차단 에러가 발생했습니다.")
    st.info(f"**상세 디버깅 에러 메시지:** {e}")