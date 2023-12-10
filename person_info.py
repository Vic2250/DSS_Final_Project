import json

import requests
import streamlit as st

data = {
    "transportatino":"567",
    "score": {
        "chinese": 0,
        "english": 0,
        "mathA": 0,
        "mathB": 0,
        "science": 0,
        "social": 0
    },
    "hope_department": "888",
}

def person_page():
    st.text('')
    st.text('')
    st.subheader('個人資料')
    st.text('')
    cols1 = st.columns([0.1, 0.9])
    label1 = cols1[0].text('國')
    chinese_score = cols1[1].number_input('國', min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols2 = st.columns([0.1, 0.9])
    label2 = cols2[0].text('英')
    english_score = cols2[1].number_input('英', min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols3 = st.columns([0.1, 0.9])
    label3 = cols3[0].text('數A')
    mathA_score = cols3[1].number_input('數A', min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols4 = st.columns([0.1, 0.9])
    label4 = cols4[0].text('數B')
    mathB_score = cols4[1].number_input('數B', min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols5 = st.columns([0.1, 0.9])
    label5 = cols5[0].text('自')
    science_score = cols5[1].number_input('自', min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols6 = st.columns([0.1, 0.9])
    label6 = cols6[0].text('社')
    social_score = cols6[1].number_input('社', min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols7 = st.columns([0.8, 0.2])
    submit = cols7[1].button('修改', use_container_width=True)
    
    if submit:
        data["score"]["chinese"] = chinese_score
        data["score"]["english"] = english_score
        data["score"]["mathA"] = mathA_score
        data["score"]["mathB"] = mathB_score
        data["score"]["science"] = science_score
        data["score"]["social"] = social_score
        print(data)
        
        response = requests.post("http://127.0.0.1:8000/getdata", data=json.dumps(data))
        if response.status_code == 200:
            st.success('輸入成功')


if __name__ == '__main__':
    person_page()
