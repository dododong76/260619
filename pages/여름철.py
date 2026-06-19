import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# 페이지 설정
st.set_page_config(page_title="☀️ 서울의 여름철 기후 분석", layout="wide")

file_name = "degree.csv"

try:
    # 데이터 로드 및 정제
    df = pd.read_csv(file_name, encoding='utf-8')
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('(℃)', '(°C)', regex=False)
    df['날짜'] = df['날짜'].astype(str).str.replace('"', '').str.replace('\t', '').str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y-%m-%d', errors='coerce')
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df = df.dropna(subset=['연도', '평균기온(°C)'])

    # ☀️ 여름철 (6월, 7월, 8월) 데이터만 필터링
    summer_df = df[df['월'].isin([6, 7, 8])]

    # 상단 헤더
    st.markdown("""
        <div style='text-align:center; padding: 20px; background-color: #FEF2F2; border-radius: 15px; margin-bottom: 25px;'>
            <h1 style='color: #DC2626; margin-bottom: 5px;'>☀️ 뜨거워지는 서울의 여름철 (6~8월)</h1>
            <p style='color: #7F1D1D; font-size: 1.1rem;'>역대 폭염의 기록과 여름 기온 우상향 트렌드 심층 분석</p>
        </div>
    """, unsafe_allow_html=True)

    # 연도별 여름 평균 기온 계산
    summer_yearly = summer_df.groupby('연도').agg({
        '평균기온(°C)': 'mean',
        '최고기온(°C)': 'max'
    }).reset_index()

    # KPI 지표
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🔥 역사상 가장 뜨거웠던 여름철 날씨 (최고기온)", 
                  value=f"{summer_df['최고기온(°C)'].max():.1f} °C",
                  delta=f"해당 일자: {summer_df.loc[summer_df['최고기온(°C)'].idxmax(), '날짜'].strftime('%Y-%m-%d')}")
    with col2:
        recent_summer_avg = summer_yearly[summer_yearly['연도'] >= 2015]['평균기온(°C)'].mean()
        st.metric(label="📊 최근 10년간 여름철 평균 기온", value=f"{recent_summer_avg:.2f} °C")
    with col3:
        # 초기 10년 대비 최근 10년 여름 기온 상승폭
        past_summer = summer_yearly[summer_yearly['연도'] < (summer_yearly['연도'].min() + 10)]['평균기온(°C)'].mean()
        recent_summer = summer_yearly[summer_yearly['연度' if '연度' in summer_yearly else '연도'] > (summer_yearly['연도'].max() - 10)]['평균기온(°C)'].mean()
        st.metric(label="📈 120년간 여름철 온도 상승 폭", value=f"+{recent_summer - past_summer:.2f} °C", delta="온난화 가속화")

    st.markdown("---")

    # 메인 시각화 (여름 평균 기온 변화 및 최고기온 변동)
    st.subheader("📈 연도별 여름철 평균 기온 및 최고 기온 추이")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=summer_yearly['연도'], y=summer_yearly['평균기온(°C)'],
        mode='lines+markers', name='여름 평균 기온', line=dict(color='#EF4444', width=2)
    ))
    
    # 추세선
    z = np.polyfit(summer_yearly['연도'], summer_yearly['평균기온(°C)'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=summer_yearly['연도'], y=p(summer_yearly['연도']),
        mode='lines', name='여름철 기온 상승 추세선', line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    
    fig.update_layout(template="plotly_white", height=450, xaxis_title="연도", yaxis_title="기온 (°C)")
    st.plotly_chart(fig, use_container_width=True)

    # 여름철 분석 데이터 탑 5
    st.subheader("☀️ 역대 가장 무더웠던 여름철 Top 5 연도")
    top_summer_years = summer_yearly.nlargest(5, '평균기온(°C)').reset_index(drop=True)
    top_summer_years.columns = ['연도', '여름철 평균기온(°C)', '해당 연도 최고기온(°C)']
    st.dataframe(top_summer_years, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 로드하는 중 에러가 발생했습니다: {e}")