import streamlit as st
import pandas as pd, numpy as np
import streamlit_antd_components as sac


# 컴포넌트 생성을 위한 함수
def create_section(header, subheaders, items, key_prefix):
    st.subheader(header)
    selected_items = []
    for idx, (subheader, item_list) in enumerate(zip(subheaders, items)):
        col1, col2 = st.columns([1,3])
        with col1:
            selected = sac.chip([
                sac.ChipItem(label=subheader)
            ], align='start', multiple=True, key=f"{key_prefix}_select_{idx}")  
        with col2:
            if len(selected) > 0:
                selected_subitems = sac.chip([
                    sac.ChipItem(label=item) for item in item_list
                ], align='start', variant='outline', multiple=True, key=f"{key_prefix}_subselect_{idx}_{len(selected)}")
                selected_items.extend(selected_subitems)
    return selected_items


def risk_function(area, eq):
    df = pd.read_excel("/Users/2ttao/Downloads/code/streamlit/docs/sbe/risk_factor.xlsx")
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
