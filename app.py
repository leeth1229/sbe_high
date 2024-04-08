import streamlit as st

##########################################################################################

st.set_page_config(
    layout="wide",
)

##########################################################################################

with st.sidebar:

    st.markdown(
        """
        ### ❓ QnA 문의
        - Cnt'-Point : \n
         여수.정비2팀 이태호 선임 \n
         여수.공무기획팀 김상협 선임 \n
         대산.공무기술팀 박웅진 선임 
        """
    )

##########################################################################################

# 탭 생성
tab1,tab2 = st.tabs(["Home","test"])

with tab1:
    st.write("# Welcome👋")
    st.markdown(
            """
            ✔️ SBE 고도화 \n
            ✔️ SBE 작성 / 강도 빈도 평가 / 엑셀 출력 \n
            \n
            - *Streamlit 은 Open Souce, 👨‍💻python 기반 GUI 입니다.*
            - *💻LG GPT 를 사용하여 초보자도 홈페이지 구성을 하실 수 가 있습니다.*
            - *기타 시각화 및 ⭐DX 기능에 대한 의견도 주시면 참고하도록 하겠습니다.*
            """
            )
