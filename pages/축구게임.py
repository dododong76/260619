import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="짜릿한 페널티킥 챌린지", page_icon="⚽", layout="centered")

st.title("⚽ 유퀴즈 미니 스포츠: 페널티킥 챌린지")
st.write("골키퍼의 움직임을 속이고 골망을 흔들어보세요! 연속 골을 넣으면 보너스 점수가 쌓입니다.")

# --- 세션 상태(Session State) 초기화 ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "combo" not in st.session_state:
    st.session_state.combo = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_status" not in st.session_state:
    st.session_state.game_status = "READY"  # READY, ANIMATION, RESULT
if "last_result" not in st.session_state:
    st.session_state.last_result = ""

# 게임 리셋 함수
def reset_soccer_game():
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.attempts = 0
    st.session_state.game_status = "READY"
    st.session_state.last_result = ""

# --- 게임 화면 구성 ---

# 상단 스코어보드 (대시보드 스타일)
st.markdown("---")
col_score1, col_score2, col_score3, col_score4 = st.columns(4)
col_score1.metric("🔥 현재 점수", f"{st.session_state.score} 골")
col_score2.metric("⚡ 연속 콤보", f"{st.session_state.combo} 연속")
col_score3.metric("🎯 총 시도 횟수", f"{st.session_state.attempts} 회")
col_score4.metric("👑 최고 기록", f"{st.session_state.high_score} 골")
st.markdown("---")

# 골대 시각화 (마크다운 가상 그래픽)
st.subheader("🥅 대한민국 국가대표 골대를 향해 슛!")

# 현재 상태에 따른 가상 그래픽 연출
if st.session_state.game_status == "READY":
    st.markdown("""
    ```text
    【=================== 골 대 ===================】
    │                                             │
    │                 🏃‍♂️ [골키퍼]                  │
    │                                             │
    └─────────────────────────────────────────────┘
                     ⚪ [축구공]
    ```
    """)
    st.info("방향을 선택하면 키커가 슛을 날립니다!")

elif st.session_state.game_status == "RESULT":
    st.markdown(st.session_state.last_result)

# --- 슛 방향 선택 및 로직 처리 ---
if st.session_state.game_status == "READY":
    st.write("### 🎯 어디로 차시겠습니까?")
    
    # 3방향 슛 버튼 배치
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    user_shoot = None
    with btn_col1:
        if st.button("⬅️ 왼쪽 구석 (Left)", use_container_width=True):
            user_shoot = "왼쪽"
    with btn_col2:
        if st.button("⬆️ 정면 강타 (Center)", use_container_width=True):
            user_shoot = "정면"
    with btn_col3:
        if st.button("➡️ 오른쪽 구석 (Right)", use_container_width=True):
            user_shoot = "오른쪽"
            
    # 사용자가 방향을 선택했을 때 경기 연산 시작
    if user_shoot is not None:
        st.session_state.attempts += 1
        
        # 골키퍼의 다이빙 방향 무작위 결정 (AI)
        gk_dive = random.choice(["왼쪽", "정면", "오른쪽"])
        
        # 로딩 스피너로 긴장감 연출
        with st.spinner("🏃‍♂️ 선수가 달려갑니다... 슈우우웃!!"):
            time.sleep(1.0) # 1초간 긴장감 조성
            
        # 결과 판정
        if user_shoot == gk_dive:
            # 골키퍼에게 막힘
            st.session_state.combo = 0
            
            # 막힌 방향에 따른 그래픽 생성
            gk_pos = {"왼쪽": "🏃‍♂️💨 [막음]       ", "정면": "       🏃‍♂️ [막음]       ", "오른쪽": "       🏃‍♂️💨 [막음]"}
            st.session_state.last_result = f"""
            ```text
            【=================== 골 대 ===================】
            │ {gk_pos[gk_dive]} │
            │                      ❌                     │
            │                  ⚽ [선방!]                  │
            └─────────────────────────────────────────────┘
            ```
            ### 😭 아쉽습니다! 골키퍼가 **{gk_dive}** 방향을 완벽하게 읽고 막아냈습니다!
            """
        else:
            # 골인 성공!
            st.session_state.score += 1
            st.session_state.combo += 1
            
            # 최고 기록 갱신 확인
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
                
            # 수비 실패한 골키퍼 위치 그래픽 생성
            gk_pos = {"왼쪽": "🏃‍♂️💨 [다이빙]                  ", "정면": "       🏃‍♂️ [정면 방어]       ", "오른쪽": "                  🏃‍♂️💨 [다이빙]"}
            ball_pos = {"왼쪽": "⚽ [GOAL!!]                                 ", "정면": "                  ⚽ [GOAL!!]                 ", "오른쪽": "                                 ⚽ [GOAL!!]"}
            
            st.session_state.last_result = f"""
            ```text
            【=================== 골 대 ===================】
            │ {ball_pos[user_shoot]} │
            │ {gk_pos[gk_dive]} │
            │                      🎉                     │
            └─────────────────────────────────────────────┘
            ```
            ### ⚽ 골 인~~~!!! 🎉
            키커는 **{user_shoot}**, 골키퍼는 **{gk_dive}**를 선택하여 완벽하게 골망을 갈랐습니다!
            """
            
        st.session_state.game_status = "RESULT"
        st.rerun()

# --- 결과 확인 및 다음 턴 진행 ---
if st.session_state.game_status == "RESULT":
    # 콤보 달성 시 특별 이펙트 세레머니
    if st.session_state.combo > 0:
        if st.session_state.combo % 3 == 0:
            st.balloons() # 3의 배수 콤보마다 풍선 세레머니
            st.success(f"🔥 대단합니다! **{st.session_state.combo}연속 골**로 해트트릭 신화를 쓰고 있습니다!")
        else:
            st.toast(f"연속 {st.session_state.combo}번째 골 성공!", icon="⚽")
            
    # 다음 슛 쏘기 버튼
    if st.button("🔄 다음 페널티킥 차기", use_container_width=True, type="primary"):
        st.session_state.game_status = "READY"
        st.rerun()

# --- 게임 리셋 및 메인 페이지 이동 ---
st.write("")
st.write("")
r_col1, r_col2 = st.columns(2)
with r_col1:
    if st.button("❌ 점수 초기화하고 다시 하기", use_container_width=True):
        reset_soccer_game()
        st.rerun()
with r_col2:
    if st.button("🏠 유퀴즈 포털(메인)로 돌아가기", use_container_width=True):
        st.switch_page("메인.py")