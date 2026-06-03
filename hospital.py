import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(page_title="Smart Hospital Patient Navigator",
                   page_icon="🏥", layout="wide")

with open("style.html", "r", encoding="utf-8") as f:
    style = f.read()
st.markdown(style, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with open('hospital_model.pkl','rb') as f:
        return pickle.load(f)

bundle        = load_model()
model         = bundle['model']
scaler        = bundle['scaler']
features      = bundle['features']
cols_to_scale = bundle['cols_to_scale']
dept_map_inv  = bundle['dept_map_inv']
gender_map    = bundle['gender_map']
temp_map      = bundle['temp_map']
hr_map        = bundle['hr_map']
dur_map       = bundle['dur_map']
cc_map        = bundle['cc_map']

DEPT_INFO = {
    'Respiratory Medicine': {
        'icon':'🫁','color':'#0284c7','bg':'#e0f2fe','border':'#7dd3fc',
        'desc':'Specialises in conditions affecting the lungs and airways.',
        'next':['Visit Level 2, Wing B','Estimated wait: 15–25 min','Please wear a mask']
    },
    'Cardiology': {
        'icon':'❤️','color':'#dc2626','bg':'#fee2e2','border':'#fca5a5',
        'desc':'Specialises in heart and cardiovascular conditions.',
        'next':['Visit Level 3, Wing A','Estimated wait: 20–30 min','Bring any previous ECG reports']
    },
    'Gastroenterology': {
        'icon':'🫃','color':'#d97706','bg':'#fef3c7','border':'#fcd34d',
        'desc':'Specialises in digestive system and abdominal conditions.',
        'next':['Visit Level 1, Wing C','Estimated wait: 10–20 min','Avoid eating before consultation']
    },
    'Neurology': {
        'icon':'🧠','color':'#7c3aed','bg':'#ede9fe','border':'#c4b5fd',
        'desc':'Specialises in brain, spine, and nervous system conditions.',
        'next':['Visit Level 4, Wing A','Estimated wait: 25–35 min','Bring list of current medications']
    },
    'General Medicine': {
        'icon':'🩺','color':'#059669','bg':'#d1fae5','border':'#6ee7b7',
        'desc':'Handles general health concerns and non-specialist conditions.',
        'next':['Visit Level 1, Wing A','Estimated wait: 10–15 min','Registration desk is open 24/7']
    },
    'Dermatology': {
        'icon':'🔬','color':'#b45309','bg':'#fef9c3','border':'#fde68a',
        'desc':'Specialises in skin, hair, and nail conditions.',
        'next':['Visit Level 2, Wing D','Estimated wait: 15–20 min','Bring photos of affected area if possible']
    },
}
with open("header.html", "r", encoding="utf-8") as f:
    header_html = f.read()

st.markdown(header_html, unsafe_allow_html=True)

with st.form("triage_form"):
    with open("symptoms.html","r",encoding="utf-8") as f:
        symptoms = f.read()
    
    st.markdown(symptoms, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        fever            = st.checkbox("🌡️  Fever")
        cough            = st.checkbox("🤧  Cough")
    with c2:
        headache = st.checkbox("Headache")
        chest_pain = st.checkbox("Chest Pain")
    with c3:
        stomach_pain = st.checkbox("Stomach Pain")
        shortness_beath = st.checkbox("Shortness of Breath")
    with c4:
        nausea_vomiting = st.checkbox("Nausea / Vomiting")
        dizziness = st.checkbox("Diziness")

    c5, _, _, _ = st.columns(4)
    with c5:
        skin_rash = st.checkbox("Skin Rash")

    st.markdown("<br>", unsafe_allow_html = True)

    with open("duration_complaint.html", "r", encoding="utf-8") as f:
        duration_complaint = f.read()
    st.markdown(duration_complaint, unsafe_allow_html = True)

    col_cc, col_dur = st.columns(2)
    with col_cc:
        chief_complaint = st.selectbox("Chief complaint", options=list(cc_map.keys()))
    with col_dur:
        duration = st.selectbox("Duration", options=list(dur_map.keys()), index=1)
    st.markdown("<br>", unsafe_allow_html=True)

    with open("severity.html", "r", encoding="utf-8") as f:
        severity = f.read()
    
    st.markdown(severity, unsafe_allow_html= True)

    col_temp, col_hr = st.columns(2)
    with col_temp:
        temprature_level = st.selectbox("Temprature", options=list(temp_map.keys()), index=1)
    with col_hr:
        heart_rate_level = st.selectbox("Heart Rate", options=list(hr_map.keys()), index=1)
    
    st.markdown("<br>", unsafe_allow_html=True)

    with open("history.html", "r", encoding="utf-8") as f:
        history = f.read()
    st.markdown(history, unsafe_allow_html=True)

    ch1, ch2, ch3, _ = st.columns(4)
    with ch1:
        hypertension = st.checkbox("High Blood Pressure")
    with ch2:
        heart_disease = st.checkbox("Heart Disease")
    with ch3:
        asthma = st.checkbox("Asthama")
    st.markdown("<br>", unsafe_allow_html=True)

    with open("patient.html", "r", encoding="utf-8") as f:
        patient = f.read()
    st.markdown(patient, unsafe_allow_html=True)
    
    col_age, col_gen = st.columns(2)
    with col_age:
        age = st.number_input("Age", min_value=1, max_value=120, value=35)
    with col_gen:
        gender = st.selectbox("Gender", options=['Female', 'Male'])
    
    submitted = st.form_submit_button("Get AI Recommendation ->")



    



