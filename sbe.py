import streamlit as st

import pandas as pd, numpy as np
import re
import os
import altair as alt
import openpyxl
from openpyxl import load_workbook
from datetime import datetime, timedelta

import streamlit_antd_components as sac

from function import risk_function
from function import create_section
from function import guide_function

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
    df_sbe_path = "/home/dataiku/workspace/code_studio-versioned/streamlit/docs/SBE/SBE_test.xlsx"
    # df_sbe_sheet_ = openpyxl.load_workbook(df_sbe_path)
    df_sbe_sheet_name_list = ["2023","2024"]
    df_sbe_sheet_name = st.selectbox("년도선택을 통해 해당년도 SBE view",df_sbe_sheet_name_list)
    # df_sbe_search1 = st.text_input("공종,공장,PR,PO 등등","")
    # df_sbe_search2 = st.text_input("SBE명,협력사명","")
    # df_sbe_search3 = st.text_input("SBE 요약 내용 검색","")

    df_sbe_ = pd.read_excel(df_sbe_path, sheet_name = df_sbe_sheet_name)
    df_sbe_ = df_sbe_.drop(["년도","No"],axis =1)
    st.data_editor(
        data = df_sbe_,
        use_container_width=True,
        column_config = {
            "PR번호":st.column_config.ListColumn(),
            "PO번호":st.column_config.ListColumn(),
            "SBE URL":st.column_config.LinkColumn(display_text="Open SBE"),
            "REF URL":st.column_config.LinkColumn(display_text="Open REF")
            }
        )

with tab3:

    st.subheader('_SBE 작성_')

    with st.container(): # 작업단계를 입력하는 섹션

        SBE_input_work_step_temp = st.text_input("작업단계", value='', placeholder='Enter Work Step')

        st.session_state['SBE_input_work_step'] = SBE_input_work_step_temp

        if 'SBE_input_work_step' in st.session_state and st.session_state['SBE_input_work_step']:
            SBE_input_work_step = st.session_state['SBE_input_work_step']  # 세션 상태에서 작업단계를 가져옴

        if st.button('선택사항 Reset'):
            st.rerun() 
            st.session_state['SBE_input_work_risk_list'] = []

    with st.container():  # 장소 / 장비공구 / 위험변수
        col31, col32, col33 = st.columns(3) 
        with col31: # 장소

            st.subheader('_1.작업환경 선택_')
            
            col31_1_1, col31_1_2 = st.columns([1,3.5]) # 장소1 - 확장
            with col31_1_1:
                SBE_input_work_area_1 = sac.chip([
                        sac.ChipItem(label='위험환경')
                        ], align='start',multiple=True, index=0)  
            with col31_1_2:
                if len(SBE_input_work_area_1) > 0:
                    SBE_input_work_area_1_ = sac.chip([
                            sac.ChipItem(label='폭발위험장소(공정구역)'),
                            sac.ChipItem(label='유해물질배출 장소'),
                            sac.ChipItem(label='고/저온물질 접촉지역')
                            ], align='start',variant='outline', multiple=True)  

            col31_2_1, col31_2_2 = st.columns([1,3.5]) # 장소2 - 확장
            with col31_2_1:
                SBE_input_work_area_2 = sac.chip([
                        sac.ChipItem(label='유해위험물질 취급')
                        ], align='start',multiple=True, index=0)  
            with col31_2_2:
                if len(SBE_input_work_area_2) > 0:
                    SBE_input_work_area_2_ = sac.chip([
                            sac.ChipItem(label='밀폐'),
                            sac.ChipItem(label='고소'),
                            sac.ChipItem(label='전기'),
                            sac.ChipItem(label='회전기계접촉'),
                            sac.ChipItem(label='차량운행'),
                            sac.ChipItem(label='중량물취급')
                            ], align='start',variant='outline', multiple=True)  

            col31_3_1, col31_3_2 = st.columns([1,3.5]) # 장소3 - 확장
            with col31_3_1:
                SBE_input_work_area_3 = sac.chip([
                        sac.ChipItem(label='특정신체영향 장소')
                        ], align='start',multiple=True, index=0)
            with col31_3_2:
                if len(SBE_input_work_area_3) > 0:
                    SBE_input_work_area_3_ = sac.chip([
                            sac.ChipItem(label='소음발생'),
                            sac.ChipItem(label='진동발생'),
                            sac.ChipItem(label='방사선발생')
                            ], align='start',variant='outline', multiple=True)  

            SBE_input_work_area_list = SBE_input_work_area_1_ + SBE_input_work_area_2_ + SBE_input_work_area_3_
            # st.session_state['SBE_input_work_area_list'] = SBE_input_work_area_list
            # st.write(st.session_state['SBE_input_work_area_list'])

        with col32: # 장비/공구

            st.subheader('_2.장비/공구 선택_')

            col32_1_1, col32_1_2 = st.columns([1,3.5]) # 장비/공구 1 - 확장
            with col32_1_1:
                SBE_input_work_eq_1 = sac.chip([
                        sac.ChipItem(label='용접/용단')
                        ], align='start',multiple=True, index=0)  
            with col32_1_2:
                if len(SBE_input_work_eq_1) > 0:
                    SBE_input_work_eq_1_ = sac.chip([
                            sac.ChipItem(label='발전용접기'),
                            sac.ChipItem(label='산소절단기')
                            ], align='start',variant='outline', multiple=True)  

            col32_2_1, col32_2_2 = st.columns([1,3.5]) # 장비/공구 2 - 확장
            with col32_2_1:
                SBE_input_work_eq_2 = sac.chip([
                        sac.ChipItem(label='중장비 사용')
                        ], align='start',multiple=True, index=0)  
            with col32_2_2:
                if len(SBE_input_work_eq_2) > 0:
                    SBE_input_work_eq_2_ = sac.chip([
                            sac.ChipItem(label='크레인'),
                            sac.ChipItem(label='고소작업차'),
                            sac.ChipItem(label='굴삭기'),
                            sac.ChipItem(label='지게차'),
                            sac.ChipItem(label='펌프카'),
                            sac.ChipItem(label='진공차'),
                            sac.ChipItem(label='Jet Car'),
                            sac.ChipItem(label='항타기/항발기/천공기')
                            ], align='start',variant='outline', multiple=True)  

            col32_3_1, col32_3_2 = st.columns([1,3.5]) # 장비/공구 3 - 확장
            with col32_3_1:
                SBE_input_work_eq_3 = sac.chip([
                        sac.ChipItem(label='전기/달기구/수공구')
                        ], align='start',multiple=True, index=0)  
            with col32_3_2:
                if len(SBE_input_work_eq_3) > 0:
                    SBE_input_work_eq_3_ = sac.chip([
                            sac.ChipItem(label='절단기'),
                            sac.ChipItem(label='파쇄기'),
                            sac.ChipItem(label='드릴'),
                            sac.ChipItem(label='발전기/케이블'),
                            sac.ChipItem(label='수공구'),
                            sac.ChipItem(label='체인블록/슬링벨트/와이어로프')
                            ], align='start',variant='outline', multiple=True)  

            col32_4_1, col32_4_2 = st.columns([1,3.5]) # 장비/공구 4 - 확장
            with col32_4_1:
                SBE_input_work_eq_4 = sac.chip([
                        sac.ChipItem(label='가설물 이용')
                        ], align='start',multiple=True, index=0)  
            with col32_4_2:
                if len(SBE_input_work_eq_4) > 0:
                    SBE_input_work_eq_4_ = sac.chip([
                            sac.ChipItem(label='가설비계(강관)'),
                            sac.ChipItem(label='가설비계(이동식)'),
                            sac.ChipItem(label='사다리(이동식)')
                            ], align='start',variant='outline', multiple=True)  

            SBE_input_work_eq_list = SBE_input_work_eq_1_ + SBE_input_work_eq_2_ + SBE_input_work_eq_3_ + SBE_input_work_eq_4_
            # st.session_state['SBE_input_work_eq_list'] = SBE_input_work_eq_list
            # st.write(st.session_state['SBE_input_work_eq_list'])

        with col33:
            try:
                # if 'SBE_input_work_risk_list' not in st.session_state:  
                st.session_state['SBE_input_work_area_list'] = SBE_input_work_area_list
                st.session_state['SBE_input_work_eq_list'] = SBE_input_work_eq_list
                SBE_input_work_risk_factors = risk_function(st.session_state['SBE_input_work_area_list'], st.session_state['SBE_input_work_eq_list'])

                risk_items = [
                                SBE_input_work_risk_factors['sames'],
                                SBE_input_work_risk_factors['risk_area'],
                                SBE_input_work_risk_factors['risk_eq'],
                                SBE_input_work_risk_factors['etcs']
                            ]
                risk_headers = ['공통 변수', '장소 변수', '장비/공구 변수', '그외 변수']
                SBE_input_work_risk_list = create_section('3.작업위험변수 선택', risk_headers, risk_items, 'work_risk')
                st.session_state['SBE_input_work_risk_list'] = SBE_input_work_risk_list
                # st.write(st.session_state['SBE_input_work_risk_list'])
            except Exception as e:
                st.error(f' Reset 버튼을 눌러주세요. : { e }') 

    with st.container(): # 작성 프레임
        # 초기 DataFrame 설정
        if 'df_sbe' not in st.session_state:
            st.session_state['df_sbe'] = pd.DataFrame({
                                                        '작업단계': [],
                                                        '작업환경': [], 
                                                        '장비/공구': [], 
                                                        '작업위험변수': []
                                                        # '유해위험요인': [], 
                                                        # '위험등급': [], 
                                                        # '감소대책': []
                                                    })
        if st.button('추가'):
            try:
                # 작업환경와 장비/공구 리스트를 문자열로 변환하고, 각 항목 사이에 쉼표를 추가하여 하나의 문자열로 합칩니다.
                # 작업 위험변수는 이미 리스트 형태로 저장되어 있으므로, 이를 사용합니다.
                작업환경_str = ', '.join(st.session_state['SBE_input_work_area_list'])
                장비공구_str = ', '.join(st.session_state['SBE_input_work_eq_list'])
                작업위험변수_list = st.session_state['SBE_input_work_risk_list']
                # 가장 긴 리스트의 길이를 기준으로 합니다.
                default_length = len(작업위험변수_list)
                # 데이터프레임 생성
                # 모든 컬럼에 대해 같은 길이를 갖도록 조정합니다.
                df_sbe_ = pd.DataFrame({
                                        '작업단계': [SBE_input_work_step] * default_length,
                                        '작업환경': [작업환경_str] * default_length,
                                        '장비/공구': [장비공구_str] * default_length,
                                        '작업위험변수': 작업위험변수_list,
                                        # '유해위험요인': [None] * default_length, 
                                        # '위험등급': [None] * default_length, 
                                        # '감소대책': [None] * default_length
                                    })

                장소_공구_list = st.session_state['SBE_input_work_area_list'] + st.session_state['SBE_input_work_eq_list']
                df_sbe_finded = guide_function(작업위험변수_list, 장소_공구_list)

                df_sbe = pd.merge(df_sbe_, df_sbe_finded, on='작업위험변수', how='outer')
                df_sbe['위험등급'] = [None] * len(df_sbe['작업위험변수'])
                df_sbe = df_sbe[['작업단계', '작업환경', '장비/공구', '작업위험변수', '유해위험요인', '위험등급', '감소대책']]

                # 생성된 데이터프레임을 세션 상태에 저장된 데이터프레임과 합칩니다.
                st.session_state['df_sbe'] = pd.concat([st.session_state['df_sbe'], df_sbe]).reset_index(drop=True)

            except Exception as e:
                st.error(f' "작업단계" 를 입력해 주세요 : { e }') 

        # Reset Cart 버튼
        if st.button('Reset'):
            st.session_state['df_sbe'] = pd.DataFrame({
                                                        '작업단계': [],
                                                        '작업환경': [], 
                                                        '장비/공구': [], 
                                                        '작업위험변수': []
                                                        # '유해위험요인': [], 
                                                        # '위험등급': [], 
                                                        # '감소대책': []
                                                    })
            st.toast('success!', icon="✅")

        edited_df_sbe = st.data_editor(st.session_state['df_sbe'], key='df_sbe_editor', num_rows="dynamic", use_container_width=True, hide_index=True)
        
        col341, col342 = st.columns([1,30])
        with col341:
            if st.button("save"):
                st.session_state['df_sbe'] = edited_df_sbe
                st.toast('success!', icon="✅")
        with col342:
            if st.button("added_SBE_Table"):
                st.session_state['SBE_Table'] = pd.concat([st.session_state['SBE_Table'], edited_df_sbe], ignore_index=True)
                st.toast('success!', icon="✅")

with tab4:
    st.subheader('_SBE Table_')

    col41,col42 = st.columns([1,5])
    with col41:
        value1 = sac.buttons([
                            sac.ButtonsItem(label='회전기계'),
                            sac.ButtonsItem(label='장치배관'),
                            sac.ButtonsItem(label='전기계장'),
                            sac.ButtonsItem(label='토목건축')
                            ],label='공종', align='start',variant='outline')  # 4가지
    with col42:
        value3 = sac.buttons([
                            sac.ButtonsItem(label='여수'),
                            sac.ButtonsItem(label='대산'),
                            sac.ButtonsItem(label='기타')
                            ],label='공종', align='start',variant='outline')  
    
    col43,col44 = st.columns(2)
    with col43:
        value4 = st.text_input("제목 입력", value='', placeholder='Vessel 철거공사 or Pump O/H')
    with col44:
        value2 = st.text_input("#소분류 입력", value='#', placeholder='Enter #기계장치_#중장비 등등')



    file_name = f"ECM_{value1}_{value2}_{value3}_{value4}_SBE.xlsx"

    st.write(file_name)




    if 'SBE_Table' not in st.session_state:
                st.session_state['SBE_Table'] = pd.DataFrame({
                                                            '작업단계': [],
                                                            '작업환경': [], 
                                                            '장비/공구': [], 
                                                            '작업위험변수': [],
                                                            '유해위험요인': [], 
                                                            '위험등급': [], 
                                                            '감소대책': []
                                                        })

    if st.button('작성내용 Reset.'):
            st.session_state['SBE_Table'] = pd.DataFrame({
                                                            '작업단계': [],
                                                            '작업환경': [], 
                                                            '장비/공구': [], 
                                                            '작업위험변수': [],
                                                            '유해위험요인': [], 
                                                            '위험등급': [], 
                                                            '감소대책': []
                                                        })
            st.toast('success!', icon="✅")

    edited_df_sbe_table = st.data_editor(st.session_state['SBE_Table'], key='df_sbe_Table_editor', use_container_width=True, hide_index=True)


    # Bulk Download Excel 버튼
    with open("sbe_final.xlsx", 'rb') as my_file:
        edited_df_sbe_table.to_excel('sbe_final.xlsx', index=False)
        st.download_button(label = 'Download SBE with format :white_check_mark:', data = my_file, file_name = file_name, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
