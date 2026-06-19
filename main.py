import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# 1. 페이지 기본 설정 및 디자인 테마 지정
st.set_page_config(
    page_title="🌍 서울 기후 타임머신: 120년의 기록",
    page_icon="🌡️",
    layout="wide"
)

# 파일 이름 매칭
file_name = "degree.csv"

try:
    # 2. 데이터 로드 및 초정밀 정제 프로세스
    df = pd.read_csv(file_name, encoding='utf-8')
    df.columns = df.columns.str.strip()
    
    # 특수문자 깨짐 및 불일치 방지를 위한 열 이름 표준화
    df.columns = df.columns.str.replace('(℃)', '(°C)', regex=False)
    
    # 날짜 열에 숨어있는 탭(\t)과 따옴표 원천 제거 후 데이트타임 변환
    df['날짜'] = df['날짜'].astype(str).str.replace('"', '').str.replace('\t', '').str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y-%m-%d', errors='coerce')
    
    # 분석용 시간 파생 변수 생성
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    
    # 결측치(데이터 구멍)가 있다면 제거
    df = df.dropna(subset=['연도', '평균기온(°C)'])

    # 3. 대시보드 메인 헤더
    st.markdown("""
        <div style='text-align:center; padding: 20px; background-color: #F8FAFC; border-radius: 15px; margin-bottom: 25px;'>
            <h1 style='color: #1E293B; font-size: 2.5rem; margin-bottom: 5px;'>🌍 서울 기후 변화 디지털 아카이브</h1>
            <p style='color: #64748B; font-size: 1.1rem;'>1907년부터 2026년까지, 기상청 데이터를 통해 본 지구온난화의 역사</p>
        </div>
    """, unsafe_allow_html=True)

    # 4. 상단 주요 인사이트 지표 (KPI Metrics)
    start_year = int(df['연도'].min())
    end_year = int(df['연도'].max())
    
    # 세기별 비교를 통한 기온 상승 폭 도출 (초기 10년 vs 최근 10년)
    past_avg = df[df['연도'] < (start_year + 10)]['평균기온(°C)'].mean()
    recent_avg = df[df['연도'] > (end_year - 10)]['평균기온(°C)'].mean()
    temp_rise = recent_avg - past_avg

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="⏳ 관측 개시 연도", value=f"{start_year}년", delta="고종 황제 재위기")
    with col2:
        st.metric(label="📅 최근 데이터 연도", value=f"{end_year}년", delta="실시간 업데이트 중")
    with col3:
        st.metric(label="🌡️ 역사상 연평균 최고 기온", value=f"{df.groupby('연도')['평균기온(°C)'].mean().max():.1f} °C")
    with col4:
        st.metric(label="🔥 120년간 평균 기온 상승", value=f"+{temp_rise:.2f} °C", delta="지구온난화 진행중", delta_color="inverse")

    st.markdown("---")

    # 대시보드 레이아웃 화면 분할 (좌측: 메인 차트 / 우측: 세부 분석)
    left_col, right_col = st.columns([2, 1])

    with left_col:
        # 5. 연도별 평균 기온 추이 메인 그래프
        st.subheader("📈 연도별 평균 기온 장기 트렌드")
        yearly_summary = df.groupby('연度' if '연度' in df else '연도')['평균기온(°C)'].mean().reset_index()
        
        fig = go.Figure()
        # 실제 변동 곡선
        fig.add_trace(go.Scatter(
            x=yearly_summary['연도'], y=yearly_summary['평균기온(°C)'],
            mode='lines+markers', name='연평균 기온',
            line=dict(color='#EF4444', width=2.5),
            marker=dict(size=4, color='#B91C1C'),
            hovertemplate='<b>%{x}년 연평균</b><br>기온: %{y:.2f}°C<extra></extra>'
        ))
        # 장기 추세선 계산 (선형 회귀선)
        z = np.polyfit(yearly_summary['연度' if '연度' in df else '연도'], yearly_summary['평균기온(°C)'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=yearly_summary['연도'], y=p(yearly_summary['연도']),
            mode='lines', name='세기적 기온 상승 추세선',
            line=dict(color='#64748B', width=2, dash='dash')
        ))
        fig.update_layout(
            xaxis_title="연도 (Year)", yaxis_title="평균 기온 (°C)",
            hovermode="x unified", template="plotly_white", height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with right_col:
        # 6. 월별 평균 기온 분포 차트 (시즌별 기온 편차 시각화)
        st.subheader("📊 월별 평균 기온 분포")
        monthly_avg = df.groupby('월')['평균기온(°C)'].mean().reset_index()
        
        fig_bar = px.bar(
            monthly_avg, x='월', y='평균기온(°C)',
            labels={'월': '월 (Month)', '평균기온(°C)': '평균 기온 (°C)'},
            color='평균기온(°C)', color_continuous_scale='Reds'
        )
        fig_bar.update_layout(template="plotly_white", height=450, showlegend=False)
        fig_bar.update_xaxes(tickmode='linear', tick0=1, dtick=1)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    
    # 7. 하단 스페셜 세션: 기후 기네스북 (익스트림 웨더)
    st.subheader("🚨 서울 기후 역대 기네스북 (Extreme Weather TOP 5)")
    kpi_col1, kpi_col2 = st.columns(2)
    
    with kpi_col1:
        st.markdown("#### ☀️ 역사상 가장 무더웠던 날 TOP 5")
        hot_days = df.nlargest(5, '최고기온(°C)')[['날짜', '최고기온(°C)', '평균기온(°C)']].reset_index(drop=True)
        hot_days['날짜'] = hot_days['날짜'].dt.strftime('%Y년 %m월 %d일')
        st.table(hot_days)
        
    with kpi_col2:
        st.markdown("#### ❄️ 역사상 가장 매서웠던 한파의 날 TOP 5")
        cold_days = df.nsmallest(5, '최저기온(°C)')[['날짜', '최저기온(°C)', '평균기온(°C)']].reset_index(drop=True)
        cold_days['날짜'] = cold_days['날짜'].dt.strftime('%Y년 %m월 %d일')
        st.table(cold_days)

    st.info("💡 **데이터 분석 정보:** 본 대시보드는 로컬의 `degree.csv` 파일을 실시간으로 정제하여 구동됩니다. 마우스를 그래프 위에 올리면 연도별 소수점 둘째 자리까지의 세부 온도 정보를 탐색할 수 있습니다.")

except Exception as e:
    st.error(f"❌ 대시보드 빌드 엔진 구동 중 에러가 발생했습니다.")
    st.info(f"**에러 로그 리포트:** {e}")