import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🌍 120년 기후 트렌드 인사이더",
    page_icon="🌡️",
    layout="wide"
)

# 파일 이름 지정
file_name = "ta_20260619190504.csv"

try:
    # 2. CSV 파일 읽기 (인코딩 처리 및 공백 자동 제거)
    # 1번째 줄부터 바로 읽기 위해 skiprows를 완전히 없앴습니다!
    df = pd.read_csv(file_name, encoding='utf-8')
    
    # 열 이름 양 끝의 미세한 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 내부의 큰따옴표 및 공백 무조건 청소하기
    df['날짜'] = df['날짜'].astype(str).str.replace('"', '').str.strip()
    
    # 안전하게 날짜 데이터타입으로 변환 후 연도 추출
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y-%m-%d', errors='coerce')
    df['연도'] = df['날짜'].dt.year

    # 3. 메인 화면 타이틀 및 스타일링
    st.markdown("""
        <div style='text-align:center; padding: 10px;'>
            <h1 style='color: #DC2626;'>🌍 지구온난화 타임머신</h1>
            <p style='color: #4B5563; font-size: 1.1rem;'>1907년부터 2026년까지의 역사적 기온 데이터 트렌드 분석</p>
        </div>
        <hr style='margin-top:0;'>
    """, unsafe_allow_html=True)

    # 데이터가 정상적으로 들어왔는지 확인
    # 복잡한 계산식 대신 데이터 존재 여부를 먼저 체크합니다.
    if df['연도'].isnull().all():
        st.error("날짜 형식을 변환하는 데 실패했습니다. 파일의 날짜 포맷을 확인해 주세요.")
    else:
        # 4. 상단 요약 지표 (KPI 메트릭) 계산
        start_year = int(df['연도'].min())
        end_year = int(df['연도'].max())
        
        # 보내주신 파일의 실제 열 이름인 '평균기온(°C)'을 매칭합니다.
        past_avg = df[df['연도'] < (start_year + 10)]['평균기온(°C)'].mean()
        recent_avg = df[df['연도'] > (end_year - 10)]['평균기온(°C)'].mean()
        temp_rise = recent_avg - past_avg

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="📊 데이터 관측 시작", value=f"{start_year}년")
        with m_col2:
            st.metric(label="📅 최근 업데이트 연도", value=f"{end_year}년")
        with m_col3:
            st.metric(label="🔥 약 120년간 평균 기온 상승", value=f"{temp_rise:.2f} °C", delta=f"{temp_rise:.2f} °C", delta_color="inverse")

        st.write("")

        # 5. 연도별 평균 기온 데이터 그룹화
        yearly_summary = df.groupby('연도')['평균기온(°C)'].mean().reset_index()

        # 6. Plotly 선 그래프 시각화
        st.subheader("📈 연도별 평균 기온 추이 선 그래프")
        
        fig = go.Figure()
        
        # 메인 변동 선
        fig.add_trace(go.Scatter(
            x=yearly_summary['연도'],
            y=yearly_summary['평균기온(°C)'],
            mode='lines+markers',
            name='연평균 기온',
            line=dict(color='#EF4444', width=2.5),
            marker=dict(size=4),
            hovertemplate='<b>%{x}년</b><br>평균 기온: %{y:.2f}°C<extra></extra>'
        ))
        
        # 장기 우상향 추세선 계산
        z = np.polyfit(yearly_summary['연도'], yearly_summary['평균기온(°C)'], 1)
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
        st.success("🎯 데이터를 성공적으로 정제하여 로컬 대시보드를 띄웠습니다!")

except Exception as e:
    st.error(f"⚠️ 데이터를 읽어오는 중 분석 엔진에 에러가 발생했습니다.")
    st.info(f"**상세 디버깅 에러 메시지:** {e}")