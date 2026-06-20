import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="실시간 세계 지진 대시보드", layout="wide")
st.title("🌋 USGS 실시간 세계 지진 검색 대시보드")
st.write("미국 지질조사국(USGS) API를 연동하여 전 세계 지진 데이터를 실시간으로 조회합니다.")

# 2. 사이드바 - 검색 조건 설정
st.sidebar.header("🔍 검색 조건 설정")

# 날짜 선택 (기본값: 최근 7일)
today = datetime.today()
seven_days_ago = today - timedelta(days=7)

start_date = st.sidebar.date_input("시작일", seven_days_ago)
end_date = st.sidebar.date_input("종료일", today)

# 최소 규모 선택 슬라이더
min_magnitude = st.sidebar.slider("최소 지진 규모 (Magnitude)", min_value=0.0, max_value=9.0, value=4.5, step=0.1)

# 검색 방식 선택 (전 세계 vs 특정 위치 반경)
search_type = st.sidebar.radio("검색 범위", ["전 세계 기준", "특정 좌표 기준 (반경)"])

params = {
    "format": "geojson",
    "starttime": start_date.strftime("%Y-%m-%d"),
    "endtime": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"), # 선택한 종료일 전체를 포함하기 위해 +1일
    "minmagnitude": min_magnitude
}

if search_type == "특정 좌표 기준 (반경)":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📍 중심 좌표 및 반경 설정")
    # 기본값은 대한민국 서울 부근 좌표
    lat = st.sidebar.number_input("위도 (Latitude)", value=36.5, min_value=-90.0, max_value=90.0)
    lon = st.sidebar.number_input("경도 (Longitude)", value=127.5, min_value=-180.0, max_value=180.0)
    radius = st.sidebar.slider("검색 반경 (km)", min_value=100, max_value=5000, value=1000, step=100)
    
    params["latitude"] = lat
    params["longitude"] = lon
    params["maxradiuskm"] = radius

# 3. API 호출 및 데이터 가공 함수
@st.cache_data(ttl=300) # 5분간 데이터 캐싱하여 성능 최적화
def get_earthquake_data(url, api_params):
    try:
        response = requests.get(url, params=api_params)
        if response.status_code == 200:
            data = response.json()
            features = data.get("features", [])
            
            # JSON에서 필요한 정보만 추출하여 리스트로 변환
            eq_list = []
            for f in features:
                props = f["properties"]
                geom = f["geometry"]
                
                # 시간 변환 (USGS는 밀리초 단위 타임스탬프를 사용함)
                epoch_time = props["time"] / 1000.0
                dt = datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
                
                eq_list.append({
                    "place": props["place"],
                    "mag": props["mag"],
                    "time": dt,
                    "latitude": geom["coordinates"][1],   # 지도의 위도 (st.map 인식용)
                    "longitude": geom["coordinates"][0],  # 지도의 경도 (st.map 인식용)
                    "depth_km": geom["coordinates"][2],
                    "url": props["url"]
                })
            return pd.DataFrame(eq_list)
        else:
            st.error(f"API 호출 실패 (오류 코드: {response.status_code})")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류 발생: {e}")
        return pd.DataFrame()

# 데이터 로드 실행
API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

with st.spinner("USGS 서버에서 지진 데이터를 가져오는 중..."):
    df = get_earthquake_data(API_URL, params)

# 4. 결과 메인 화면 시각화
if not df.empty:
    # 상단 요약 지표 (Metrics)
    total_count = len(df)
    max_mag = df["mag"].max()
    max_place = df.loc[df["mag"].idxmax(), "place"]
    
    col1, col2 = st.columns(2)
    col1.metric(label="📊 조건 내 검색된 지진 횟수", value=f"{total_count} 건")
    col2.metric(label="🚨 가장 강한 지진 규모", value=f"M {max_mag}", delta=max_place, delta_color="inverse")
    
    st.markdown("---")
    
    # 레이아웃 나누기 (좌측: 지도, 우측: 데이터 표)
    map_col, data_col = st.columns([3, 2])
    
    with map_col:
        st.subheader("🗺️ 지진 발생 위치 지도")
        st.write("점의 위치에서 지진이 발생했습니다. (확대/축소 가능)")
        
        # 1. 데이터프레임에 'marker_size'라는 이름의 새로운 컬럼을 만듭니다.
        df["marker_size"] = df["mag"] * 10  # 가시성을 위해 곱하는 숫자를 10으로 조금 키웠습니다.
        
        # 2. size 인자에는 컬럼의 '이름(문자열)'만 적어줍니다.
        st.map(df, size="marker_size")
        
    with data_col:
        st.subheader("📋 지진 상세 리스트 (최근 순)")
        # 화면에 보여줄 칼럼 순서 정돈
        display_df = df[["time", "mag", "place", "depth_km"]]
        st.dataframe(display_df, use_container_width=True, height=450)
        
    # 다운로드 기능 추가
    st.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 검색 결과 CSV 다운로드",
        data=csv,
        file_name=f"usgs_earthquakes_{start_date}_to_{end_date}.csv",
        mime="text/csv"
    )

else:
    st.info("선택하신 조건에 해당하는 지진 데이터가 없습니다. 규모를 낮추거나 기간을 늘려보세요.")