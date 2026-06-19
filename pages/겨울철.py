import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# 페이지 설정
st.set_page_config(page_title="❄️ 서울의 겨울철 기후 분석", layout="wide")

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

    # ❄️ 겨울철 (12월, 1월, 2월) 데이터 필터링
    # 주의: 기상학적으로 2025년 12월 ~ 2026년 2월을 한 겨울로 보나, 단순 월별 필터링으로 처리합니다.
    winter_df = df[df['월'].isin([12, 1, 2])]

    # 상단 헤더
    st.markdown("""
        <div style='text-align:center; padding: 20px; background-color: #F0FDF4; border-radius: 15px; margin-bottom: 25px;'>
            <h1 style='color: #16A34A; margin-bottom: 5px;'>❄️ 사라져가는 서울의 삼한사온 (12~2월)</h1>
            <p style='color: #14532D; font-size: 1.1rem;'>역대 한파 기록 및 겨울철 기온 상승과 변동성 분석</p>
        </div>
    """, unsafe_allow_html=True)

    # 연도별 겨울 평균 및 최저 기온 계산
    winter_yearly = winter_df.groupby('연도').agg({
        '평균기온(°C)': 'mean',
        '최저기온(°C)': 'min'
    }).reset_index()

    # KPI 지표
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🥶 역사상 가장 추웠던 겨울철 날씨 (최저기온)", 
                  value=f"{winter_df['최저기온(°C)'].min():.1f} °C",
                  delta=f"해당 일자: {winter_df.loc[winter_df['최저기온(°C)'].idxmin(), '날짜'].strftime('%Y-%m-%d')}")
    with col2:
        recent_winter_avg = winter_yearly[winter_yearly['연도'] >= 2015]['평균기온(°C)'].mean()
        st.metric(label="📊 최근 10년간 겨울철 평균 기온", value=f"{recent_winter_avg:.2f} °C")
    with col3:
        # 초기 10년 대비 최근 10년 겨울 기온 상승폭
        past_winter = winter_yearly[winter_yearly['연도'] < (winter_yearly['연도'].min() + 10)]['평균기온(°C)'].mean()
        recent_winter = winter_yearly[winter_yearly['연도'] > (winter_yearly['연도'].max() - 10)]['평균기온(°C)'].mean()
        st.metric(label="📈 120년간 겨울철 온도 상승 폭", value=f"+{recent_winter - past_winter:.2f} °C", delta="겨울 실종 우려", delta_color="inverse")

    st.markdown("---")

    # 메인 시각화 (겨울 평균 기온 변화 및 최저기온 변동)
    st.subheader("📈 연도별 겨울철 평균 기온 및 최저 기온 추이")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=winter_yearly['연도'], y=winter_yearly['평균기온(°C)'],
        mode='lines+markers', name='겨울 평균 기온', line=dict(color='#2563EB', width=2)
    ))
    
    # 추세선
    z = np.polyfit(winter_yearly['연도'], winter_yearly['평균기온(°C)'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=winter_yearly['연度' if '연度' in winter_yearly else '연도'], y=p(winter_yearly['연도']),
        mode='lines', name='겨울철 기온 상승 추세선', line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    
    fig.update_layout(template="plotly_white", height=450, xaxis_title="연도", yaxis_title="기온 (°C)")
    st.plotly_chart(fig, use_container_width=True)

    # 겨울철 분석 데이터 탑 5
    st.subheader("❄️ 역대 가장 따뜻했던(지구온난화 영향) 겨울철 Top 5 연도")
    top_winter_years = winter_yearly.nlargest(5, '평균기온(°C)').reset_index(drop=True)
    top_winter_years.columns = ['연도', '겨울철 평균기온(°C)', '해당 연도 최저기온(°C)']
    st.dataframe(top_winter_years, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 로드하는 중 에러가 발생했습니다: {e}")