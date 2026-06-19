import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.title("🌡️ 120년 기후 데이터 분석 엔진")

# 1. 파일이 진짜 존재하는지 경로 체크
file_name = "ta_20260619190504.csv"

if not os.path.exists(file_name):
    st.error(f"❌ '{file_name}' 파일을 찾을 수 없습니다.")
    st.info(f"현재 프로그램이 인식하는 폴더 위치: `{os.getcwd()}`\n\n이 폴더 안에 해당 CSV 파일이 들어있는지 확인해 주세요!")
else:
    try:
        # 2. 첫 번째 시도: 안내문이 포함된 기상청 원본 파일 포맷으로 읽기
        df = pd.read_csv(file_name, encoding='cp949', skiprows=7)
        
        # 만약 skiprows 때문에 컬럼이 깨졌다면 skiprows 없이 다시 읽기
        if '날짜' not in df.columns and '평균기온(℃)' not in "".join(df.columns):
            df = pd.read_csv(file_name, encoding='cp949')
            
        # 컬럼명 공백 제거
        df.columns = df.columns.str.strip()
        
        # 3. 필수 컬럼이 존재하느냐 검사
        # 기상청 최신 포맷은 '평균기온(℃)' 입니다. (특수문자 주의)
        target_col = [col for col in df.columns if '평균기온' in col]
        
        if not target_col:
            st.error("❌ CSV 파일 안에서 '평균기온' 열을 찾을 수 없습니다.")
            st.write("현재 파일에 존재하는 열 이름들:", list(df.columns))
        else:
            actual_temp_col = target_col[0]
            df['날짜'] = pd.to_datetime(df['날짜'])
            df['연도'] = df['날짜'].dt.year
            
            # 4. 연도별 그룹화 데이터 연산
            yearly_summary = df.groupby('연도')[actual_temp_col].mean().reset_index()
            
            # 5. 그래프 시각화
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=yearly_summary['연도'],
                y=yearly_summary[actual_temp_col],
                mode='lines+markers',
                name='연평균 기온',
                line=dict(color='#EF4444')
            ))
            fig.update_layout(xaxis_title="연도", yaxis_title="평균 기온 (°C)", template="plotly_white")
            
            st.plotly_chart(fig, use_container_width=True)
            st.success("🎯 데이터를 성공적으로 읽어와 차트를 그렸습니다!")

    except Exception as e:
        st.error(f"❌ 코드는 파일을 찾았으나 내부 데이터를 해석하는 도중 에러가 났습니다.")
        st.code(f"에러 내용: {e}")