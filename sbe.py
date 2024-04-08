import streamlit as st

import pandas as pd, numpy as np
import altair as alt

import streamlit_antd_components as sac

from function_sbe import create_section
from function_sbe import risk_function


st.set_page_config(
    layout="wide",
    page_title="Hello",
    page_icon="👋",
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
tab1, tab2, tab3, tab4, tab5  = st.tabs(["SBE Monitoring", "공무.SBE 현황", "SBE 작성", "SBE 결과", "Help" ])

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

with tab2:
    st.header("공무.SBE 현황표")

with tab3:
    st.subheader('_SBE 작성_')

    # 작업단계를 입력하는 섹션
    with st.container():
        SBE_input_work_step_temp = st.text_input("작업단계", value='', placeholder='Enter Work Step')
        st.session_state['SBE_input_work_step'] = SBE_input_work_step_temp
        if st.button("reset"):
            st.rerun()

    if 'SBE_input_work_step' in st.session_state and st.session_state['SBE_input_work_step']:
        SBE_input_work_step = st.session_state['SBE_input_work_step']  # 세션 상태에서 작업단계를 가져옴

        with st.container():  # 장소 섹션
            col31, col32, col33 = st.columns([1, 1, 1])
            with col31:
                if 'SBE_input_work_area_list' not in st.session_state:
                    st.session_state['SBE_input_work_area_list'] = []
                place_headers = ['위험장소', '유해위험물질취급 장소', '특정 신체영향 장소']
                place_items = [
                    ['폭발위험장소(공정구역)', '유해물질 배출 장소', '고/저온물질 접촉지역'],
                    ['밀폐', '고소', '전기', '회전기계접촉', '차량운행', '중량물취급'],
                    ['소음발생', '진동발생', '방사선발생']
                ]
                SBE_input_work_area_list = create_section('1.작업장소 선택', place_headers, place_items, 'work_area')
                st.session_state['SBE_input_work_area_list'] = SBE_input_work_area_list
                st.write(st.session_state['SBE_input_work_area_list'])

        with st.container():  # 장비/공구 섹션
            with col32:
                if 'SBE_input_work_eq_list' not in st.session_state:
                    st.session_state['SBE_input_work_eq_list'] = []
                equipment_headers = ['용접/용단', '중장비 사용', '전기/달기구/수공구', '가설물 이용']
                equipment_items = [
                    ['발전용접기', '산소절단기'],
                    ['크레인', '고소작업차', '굴삭기', '지게차', '펌프카', '진공차', 'Jet Car', '항타기/항발기/천공기'],
                    ['절단기', '파쇄기', '드릴', '발전기/케이블', '수공구', '체인블록/슬링벨트/와이어로프'],
                    ['가설비계(강관)', '가설비계(이동식)', '사다리(이동식)']
                ]
                SBE_input_work_eq_list = create_section('2.장비/공구 선택', equipment_headers, equipment_items, 'work_eq')
                st.session_state['SBE_input_work_eq_list'] = SBE_input_work_eq_list
                st.write(st.session_state['SBE_input_work_eq_list'])

        with st.container():  # 작업 위험 변수 섹션
            with col33:
                if 'SBE_input_work_risk_list' not in st.session_state:
                    st.session_state['SBE_input_work_risk_list'] = []
                risk_headers = ['공통 변수', '장소 변수', '장비/공구 변수', '그외 변수']
                SBE_input_work_risk_factors = risk_function(st.session_state['SBE_input_work_area_list'], st.session_state['SBE_input_work_eq_list'])
                risk_items = [
                    SBE_input_work_risk_factors['sames'],
                    SBE_input_work_risk_factors['risk_area'],
                    SBE_input_work_risk_factors['risk_eq'],
                    SBE_input_work_risk_factors['etcs']
                ]
                SBE_input_work_risk_list = create_section('3.작업위험변수 선택', risk_headers, risk_items, 'work_risk')
                st.session_state['SBE_input_work_risk_list'] = SBE_input_work_risk_list
                st.write(st.session_state['SBE_input_work_risk_list'])


        with st.container():
            if st.button('추가'):
                # 초기 DataFrame 설정
                if 'df_sbe' not in st.session_state:
                    st.session_state['df_sbe'] = pd.DataFrame({
                        '작업단계': [],
                        '작업장소': [], 
                        '장비/공구': [], 
                        '작업위험변수': [], 
                        '유해작업요인': [], 
                        '위험등급': [], 
                        '감소대책': []
                    })
                # 작업장소와 장비/공구 리스트를 문자열로 변환하고, 각 항목 사이에 쉼표를 추가하여 하나의 문자열로 합칩니다.
                # 작업 위험변수는 이미 리스트 형태로 저장되어 있으므로, 이를 사용합니다.
                작업장소_str = ', '.join(st.session_state['SBE_input_work_area_list'])
                장비공구_str = ', '.join(st.session_state['SBE_input_work_eq_list'])
                작업위험변수_list = st.session_state['SBE_input_work_risk_list']

                # 가장 긴 리스트의 길이를 기준으로 합니다.
                default_length = len(작업위험변수_list)

                # 데이터프레임 생성
                # 모든 컬럼에 대해 같은 길이를 갖도록 조정합니다.
                df_sbe = pd.DataFrame({
                    '작업단계': [SBE_input_work_step] * default_length,
                    '작업장소': [작업장소_str] * default_length,
                    '장비/공구': [장비공구_str] * default_length,
                    '작업위험변수': 작업위험변수_list,
                    '유해작업요인': [None] * default_length, 
                    '위험등급': [None] * default_length, 
                    '감소대책': [None] * default_length
                })

                # 생성된 데이터프레임을 세션 상태에 저장된 데이터프레임과 합칩니다.
                st.session_state['df_sbe'] = pd.concat([st.session_state['df_sbe'], df_sbe]).reset_index(drop=True)

    with st.container():
        # st.data_editor 대신 st.dataframe 사용
        edited_df_sbe = st.data_editor(st.session_state['df_sbe'], key='df_sbe_editor', num_rows="dynamic", use_container_width=True, hide_index=True)
        if st.session_state['df_sbe'] is not None:
            st.session_state['df_sbe'] = edited_df_sbe
