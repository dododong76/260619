import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="🌍 120년 기후 트렌드 인사이더",
    page_icon="🌡️",
    layout="wide"
)

# 2. GitHub CSV 데이터 로드 함수
# @st.cache_data를 사용하면 앱이 새로고침될 때마다 무겁게 깃허브에서 데이터를 다시 읽어오지 않아 속도가 빨라집니다.
@st.cache_data
def load_data(url):
    # 깃허브 raw 주소로부터 csv 파일 읽기
    df = pd.read_csv(url)
    
    # '날짜' 열을 파이썬 데이트타임 형태로 변환 (연도 추출을 위해 필수)
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    # 분석에 사용할 '연도' 열 추가
    df['연도'] = df['날짜'].dt.year
    return df

# ⚠️ [중요] 본인의 파일명에 맞게 URL 맨 뒷부분 'weather_data.csv'를 실제 파일명으로 수정해주세요!
csv_url = "https://raw.githubusercontent.com/dododong76/260619/main/weather_data.csv"

try:
    df = load_data(csv_url)
    
    # 3. 메인 화면 타이틀 및 스타일링
    st.markdown("""
        <div style='text-align:center; padding: 10px;'>
            <h1 style='color: #DC2626;'>🌍 지구온난화 타임머신</h1>
            <p style='color: #4B5563; font-size: 1.1rem;'>1907년부터 2026년까지의 역사적 기온 데이터 트렌드 분석</p>
        </div>
        <hr style='margin-top:0;'>
    """, unsafe_allow_html=True)

    # 4. 상단 요약 지표 (KPI 메트릭) 계산
    # 데이터의 시작 연도와 끝 연도 자동 추출
    start_year = int(df['연도'].min())
    end_year = int(df['연도'].max())
    
    # 과거 10년 vs 최근 10년 평균 기온 비교를 통한 상승 폭 계산
    past_avg = df[df['연도'] < (start_year + 10)]['평균 기온'].mean()
    recent_avg = df[df['연도'] > (end_year - 10)]['평균 기온'].mean()
    temp_rise = recent_avg - past_avg

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="📊 데이터 관측 시작", value=f"{start_year}년")
    with m_col2:
        st.metric(label="📅 최근 업데이트 연도", value=f"{end_year}년")
    with m_col3:
        st.metric(label="🔥 약 120년간 평균 기온 상승", value=f"{temp_rise:.2f} °C", delta=f"{temp_rise:.2f} °C", delta_color="inverse")

    st.write("")

    # 5. 연도별 평균 기온 데이터 그룹화 연산
    # '연도' 기준으로 묶어서 '평균 기온'의 평균값을 구합니다.
    yearly_summary = df.groupby('연o')['평균 기온'].mean().reset_index()

    # 6. Plotly 선 그래프(Line Chart) 시각화 룸
    st.subheader("📈 연도별 평균 기온 추이 선 그래프")
    
    # 대화형 그래프 빌드
    fig = go.Figure()
    
    # 메인 변동 선 추가
    fig.add_trace(go.Scatter(
        x=yearly_summary['연도'],
        y=yearly_summary['평균 기온'],
        mode='lines+markers',
        name='연평균 기온',
        line=dict(color='#EF4444', width=2.5),
        marker=dict(size=4),
        hovertemplate='<b>%{x}년</b><br>평균 기온: %{y:.2f}°C<extra></extra>'
    ))
    
    # 전체 흐름을 보기 위한 추세선(경향선) 추가 (선택 사항)
    # 간단한 선형 추세를 보기 위해 일차 방정식 핏팅 기법을 가미합니다.
    import numpy as np
    z = np.polyfit(yearly_summary['연도'], yearly_summary['평균 기온'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=yearly_summary['연도'],
        y=p(yearly_summary['연도']),
        mode='lines',
        name='장기 상승 추세선',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))

    # 그래프 레이아웃 다듬기
    fig.update_layout(
        xaxis_title="연도 (Year)",
        yaxis_title="평균 기온 (°C)",
        hovermode="x unified",
        template="plotly_white",
        height=500,
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # 스트림릿 화면에 그래프 렌더링
    st.plotly_chart(fig, use_container_width=True)
    
    # 7. 하단 안내 보조 지표
    st.info("💡 **그래프 활용 팁:** 마우스를 그래프 선 위에 올리면(Hover) 해당 연도의 정확한 평균 기온을 실시간으로 확인할 수 있으며, 차트 우측 상단 툴바를 이용해 특정 구간만 드래그하여 확대 분석할 수 있습니다.")

except Exception as e:
    st.error(f"⚠️ 데이터를 불러오거나 분석하는 중 에러가 발생했습니다.")