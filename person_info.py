import json

import requests
import streamlit as st

data = {
    "transportation":"567",
    "info": {
        "國": {"score": 0, "rank": ""},
        "英": {"score": 0, "rank": ""},
        "數A": {"score": 0, "rank": ""},
        "數B": {"score": 0, "rank": ""},
        "自": {"score": 0, "rank": ""},
        "社": {"score": 0, "rank": ""},
    },
    "listen" : {"score": "", "rank": ""},
    "hope_department": "888",
}

#英聽成績
listen_score = ["A", "B", "C", "F"]


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
    cols7 = st.columns([0.1, 0.9])
    label7 = cols7[0].text('英聽')
    listen_selectbox = cols7[1].selectbox('英聽', listen_score, index=0, label_visibility='collapsed')
    cols8 = st.columns([0.8, 0.2])
    submit = cols8[1].button('修改', use_container_width=True)
    
    
    if submit:
        data["info"]["國"]["score"] = chinese_score
        data["info"]["英"]["score"] = english_score
        data["info"]["數A"]["score"] = mathA_score
        data["info"]["數B"]["score"] = mathB_score
        data["info"]["自"]["score"] = science_score
        data["info"]["社"]["score"] = social_score
        data["listen"]["score"] = listen_selectbox
        #print(data)
        
        response = requests.post("http://127.0.0.1:8000/getdata", data=json.dumps(data))
        if response.status_code == 200:
            st.success('輸入成功')


if __name__ == '__main__':
    person_page()
