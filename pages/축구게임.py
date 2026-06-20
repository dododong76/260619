import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 앱을 전체 화면(와이드 모드)으로 설정
st.set_page_config(layout="wide")

# 삽입할 GlowScript URL
url = "https://www.glowscript.org/#/user/kyungdong/folder/MyPrograms/program/worldcup03"

# 2. iframe 및 주변 여백을 완전히 제거하는 HTML/CSS 작성
# scrolling="no"와 overflow:hidden을 통해 스크롤바를 강제로 숨깁니다.
iframe_html = f"""
<style>
    html, body {{
        margin: 0;
        padding: 0;
        overflow: hidden;
        height: 100%;
        width: 100%;
    }}
    iframe {{
        border: none;
        width: 100%;
        height: 100%;
    }}
</style>
<iframe 
    src="{url}" 
    scrolling="no"
    allowfullscreen
>
</iframe>
"""

# 3. Streamlit 컴포넌트 배치
# height 값을 800~900 정도로 넉넉하게 주면 GlowScript 화면이 시원하게 커집니다.
components.html(iframe_html, height=800)