import streamlit as st
import pandas as pd, numpy as np
import streamlit_antd_components as sac

@st.cache_data
def risk_function(area, eq):
    df = pd.read_excel("/home/dataiku/workspace/code_studio-versioned/streamlit/docs/risk_factors/risk_factor.xlsx")
    risk_area = []
    for i in range(len(area)):
        risk_area.append(df[df["위험인자"] == area[i]]["위험변수"].tolist())

    risk_area = set([item for sublist in risk_area for item in sublist])

    risk_eq = []
    for i in range(len(eq)):
        risk_eq.append(df[df["위험인자"] == eq[i]]["위험변수"].tolist())

    risk_eq = set([item for sublist in risk_eq for item in sublist])

    sames = list(risk_area.intersection(risk_eq))
    risk_area = list(risk_area.difference(sames))
    risk_eq = list(risk_eq.difference(sames))

    all_risk_factors = ["추락","전도","충돌","낙하/비래","붕괴","산소결핍","화학물질 흡입", "이상온도/물체 접촉","감전", "건강장애 위험(시력/청력/피부)", "화재","폭발","정전기 발생", "설비파손(파열)", "누출", "기타(환경사고 등)", "협착", "절단/베임/찔림"]
    etcs = list(set(all_risk_factors).difference(sames).difference(risk_area).difference(risk_eq))

    return {"sames": sames, "risk_area": risk_area, "risk_eq": risk_eq, "etcs": etcs}


# 컴포넌트 생성을 위한 함수
def create_section(header, subheaders, items, key_prefix):
    st.subheader(header)
    selected_items = []
    for idx, (subheader, item_list) in enumerate(zip(subheaders, items)):
        col1, col2 = st.columns([1,3.5])
        with col1:
            selected = sac.chip([
                    sac.ChipItem(label=subheader)
                ], index = 0 ,align='start', multiple=True, key=f"{key_prefix}_select_{idx}")  
        with col2:
            if len(selected) > 0:
                selected_subitems = sac.chip([
                    sac.ChipItem(label=item) for item in item_list
                ], align='start', variant='outline', multiple=True, key=f"{key_prefix}_subselect_{idx}_{len(selected)}")
                selected_items.extend(selected_subitems)
    return selected_items

@st.cache_data
def guide_function(risk_factor, area_n_eq):
    df = pd.read_excel("/home/dataiku/workspace/code_studio-versioned/streamlit/docs/risk_factors/guide_factor.xlsx")

    risk_guide = []
    safety_guide = []
    for i in range(len(risk_factor)):
        for j in range(len(area_n_eq)):
            risk_guide.append(df[(df["작업위험변수"] == risk_factor[i]) & (df["장소/공구"] == area_n_eq[j])]["유해위험요인"].tolist())
            safety_guide.append(df[(df["작업위험변수"] == risk_factor[i]) & (df["장소/공구"] == area_n_eq[j])]["감소대책"].tolist())

    df_ = pd.DataFrame()
    # df_["작업위험변수"] = risk_factor
    df_["유해위험요인"] = risk_guide
    df_["감소대책"] = safety_guide

    def group_values(df):
        new_dict = {}
        for col in df.columns:
            values = df[col].tolist()
            new_values = []
            for value in values:
                if isinstance(value, list):
                    new_values.append(value)
                elif value not in new_values:
                    new_values.append(value)
            new_dict[col] = new_values
        return pd.DataFrame(new_dict)

    df_new = group_values(df_)

    return df_new


# 작업환경와 장비/공구 리스트를 문자열로 변환하고, 각 항목 사이에 쉼표를 추가하여 하나의 문자열로 합칩니다.
# 작업 위험변수는 이미 리스트 형태로 저장되어 있으므로, 이를 사용합니다.
작업환경_str = ', '.join(st.session_state['SBE_input_work_area_list'])
장비공구_str = ', '.join(st.session_state['SBE_input_work_eq_list'])
작업위험변수_list = st.session_state['SBE_input_work_risk_list']


# 가장 긴 리스트의 길이를 기준으로 합니다.
default_length = len(작업위험변수_list)
if st.button('추가'):
    try:
        # 작업환경와 장비/공구 리스트를 문자열로 변환하고, 각 항목 사이에 쉼표를 추가하여 하나의 문자열로 합칩니다.
        # 작업 위험변수는 이미 리스트 형태로 저장되어 있으므로, 이를 사용합니다.
        작업환경_str = ', '.join(st.session_state['SBE_input_work_area_list'])
        장비공구_str = ', '.join(st.session_state['SBE_input_work_eq_list'])
        작업위험변수_list = st.session_state['SBE_input_work_risk_list']
        # 가장 긴 리스트의 길이를 기준으로 합니다.

        장소_공구_list = st.session_state['SBE_input_work_area_list'] + st.session_state['SBE_input_work_eq_list']
        st.write(작업위험변수_list)
        st.write(장소_공구_list)
        df_new = guide_function(작업위험변수_list, 장소_공구_list)
        st.write(df_new)
        
        default_length = len(df_new["유해위험요인"])

        # 데이터프레임 생성
        # 모든 컬럼에 대해 같은 길이를 갖도록 조정합니다.
        df_sbe = pd.DataFrame({
                                '작업단계': [SBE_input_work_step] * default_length,
                                '작업환경': [작업환경_str] * default_length,
                                '장비/공구': [장비공구_str] * default_length,
                                '작업위험변수': 작업위험변수_list,
                                '유해위험요인': [None] * df_new["유해위험요인"], 
                                '위험등급': [None] * default_length, 
                                '감소대책': [None] * df_new["감소대책"]
                            })

        # 생성된 데이터프레임을 세션 상태에 저장된 데이터프레임과 합칩니다.
        st.session_state['df_sbe'] = pd.concat([st.session_state['df_sbe'], df_sbe]).reset_index(drop=True)
