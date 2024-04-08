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
from function import ChipItems

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

    # 작업단계를 입력
    SBE_input_work_step = st.text_input("작업단계", value = '', placeholder='Enter Work Step')

    if SBE_input_work_step != '': # 작업 단계가 입력 되면

        col31, col32, col34 = st.columns(3) # 장소 / 장비공구 / 위험 변수
        with col31: # 장소

            st.subheader('_1.작업장소 선택_')
            
            col31_1_1, col31_1_2 = st.columns([1,3]) # 장소1 - 확장
            with col31_1_1:
                SBE_input_work_area_1 = sac.chip([
                        sac.ChipItem(label='위험장소')
                        ], align='start',multiple=True, index=0)  
            with col31_1_2:
                if len(SBE_input_work_area_1) > 0:
                    SBE_input_work_area_1_ = sac.chip([
                            sac.ChipItem(label='폭발위험장소(공정구역)'),
                            sac.ChipItem(label='유해물질 배출 장소'),
                            sac.ChipItem(label='고/저온물질 접촉지역')
                            ], align='start',variant='outline', multiple=True)  

            col31_2_1, col31_2_2 = st.columns([1,3]) # 장소2 - 확장
            with col31_2_1:
                SBE_input_work_area_2 = sac.chip([
                        sac.ChipItem(label='유해위험물질취급 장소')
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

            col31_3_1, col31_3_2 = st.columns([1,3]) # 장소3 - 확장
            with col31_3_1:
                SBE_input_work_area_3 = sac.chip([
                        sac.ChipItem(label='특정 신체영향 장소')
                        ], align='start',multiple=True, index=0)
            with col31_3_2:
                if len(SBE_input_work_area_3) > 0:
                    SBE_input_work_area_3_ = sac.chip([
                            sac.ChipItem(label='소음발생'),
                            sac.ChipItem(label='진동발생'),
                            sac.ChipItem(label='방사선발생')
                            ], align='start',variant='outline', multiple=True)  

            SBE_input_work_area_list = SBE_input_work_area_1_ + SBE_input_work_area_2_ + SBE_input_work_area_3_
            st.write(SBE_input_work_area_list)

        with col32: # 장비/공구

            st.subheader('_2.장비/공구 선택_')

            col32_1_1, col32_1_2 = st.columns([1,3]) # 장비/공구 1 - 확장
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

            col32_2_1, col32_2_2 = st.columns([1,3]) # 장비/공구 2 - 확장
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

            col32_3_1, col32_3_2 = st.columns([1,3]) # 장비/공구 3 - 확장
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

            col32_4_1, col32_4_2 = st.columns([1,3]) # 장비/공구 4 - 확장
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
            st.write(SBE_input_work_eq_list)

        
        with col34: #작업 위험 변수 

            st.subheader('_3.작업위험변수 선택_')

            SBE_input_work_risk_factors = risk_function(SBE_input_work_area_list,SBE_input_work_eq_list)

            col34_1_1, col34_1_2 = st.columns([1,3]) # 작업위험변수 1 - 확장
            with col34_1_1:
                SBE_input_work_risk_1 = sac.chip([
                        sac.ChipItem(label='공통 변수')
                        ], align='start',multiple=True, key="unique_key5")  
            with col34_1_2:
                if len(SBE_input_work_risk_1) > 0:
                    SBE_input_work_risk_1_ = sac.chip(ChipItems(SBE_input_work_risk_factors['sames']), align='start', variant='outline', multiple=True, key="unique_key1")

            col34_2_1, col34_2_2 = st.columns([1,3]) # 작업위험변수 2 - 확장
            with col34_2_1:
                SBE_input_work_risk_2 = sac.chip([
                        sac.ChipItem(label='장소 변수')
                        ], align='start',multiple=True,  key="unique_key6")  
            with col34_2_2:
                if len(SBE_input_work_risk_2) > 0:
                    SBE_input_work_risk_2_ = sac.chip(ChipItems(SBE_input_work_risk_factors['risk_area']), align='start', variant='outline', multiple=True, key="unique_key2")

            col34_3_1, col34_3_2 = st.columns([1,3]) # 작업위험변수 3 - 확장
            with col34_3_1:
                SBE_input_work_risk_3 = sac.chip([
                        sac.ChipItem(label='장비/공구 변수')
                        ], align='start',multiple=True, key="unique_key7")  
            with col34_3_2:
                if len(SBE_input_work_risk_3) > 0:
                    SBE_input_work_risk_3_ = sac.chip(ChipItems(SBE_input_work_risk_factors['risk_eq']), align='start', variant='outline', multiple=True, key="unique_key3")

            col34_4_1, col34_4_2 = st.columns([1,3]) # 작업위험변수 4 - 확장
            with col34_4_1:
                SBE_input_work_risk_4 = sac.chip([
                        sac.ChipItem(label='그외 변수')
                        ], align='start',multiple=True, key="unique_key8")  
            with col34_4_2:
                if len(SBE_input_work_risk_4) > 0:
                    SBE_input_work_risk_4_ = sac.chip(ChipItems(SBE_input_work_risk_factors['etcs']), align='start', variant='outline', multiple=True, key="unique_key4")        

     



