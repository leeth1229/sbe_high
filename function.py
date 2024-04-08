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

@st.cache_data
def ChipItems(items):
    chip_items = [sac.ChipItem(label=item) for item in items]
    return chip_items
