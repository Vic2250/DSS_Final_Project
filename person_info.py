import json
import requests
import streamlit as st

#英聽成績
listen_data = ["A", "B", "C", "F"]


def check_grade(grade):
    if grade == 'A':
        return 0
    elif grade == 'B':
        return 1
    elif grade == 'C':
        return 2
    else:
        return 3


def person_page():
    st.text('')
    st.text('')
    st.title('個人資料')
    st.text('')
    config_data = get_info()
    config_data['英聽']['score'] = check_grade(config_data['英聽']['score'])
    cols1 = st.columns([0.1, 0.9])
    label1 = cols1[0].subheader('國')
    chinese_score = cols1[1].number_input('國', value=config_data['國文']['score'], min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols2 = st.columns([0.1, 0.9])
    label2 = cols2[0].subheader('英')
    english_score = cols2[1].number_input('英', value=config_data['英文']['score'], min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols3 = st.columns([0.1, 0.9])
    label3 = cols3[0].subheader('數A')
    mathA_score = cols3[1].number_input('數A', value=config_data['數A']['score'], min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols4 = st.columns([0.1, 0.9])
    label4 = cols4[0].subheader('數B')
    mathB_score = cols4[1].number_input('數B', value=config_data['數B']['score'], min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols5 = st.columns([0.1, 0.9])
    label5 = cols5[0].subheader('自')
    science_score = cols5[1].number_input('自', value=config_data['自然']['score'], min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols6 = st.columns([0.1, 0.9])
    label6 = cols6[0].subheader('社')
    social_score = cols6[1].number_input('社', value=config_data['社會']['score'], min_value=0, max_value=15, step=1, label_visibility='collapsed')
    cols7 = st.columns([0.1, 0.9])
    label7 = cols7[0].subheader('英聽')
    listen_score = cols7[1].selectbox('英聽', listen_data, index=config_data['英聽']['score'], label_visibility='collapsed')
    
    #
    title = st.columns([1, 1])
    title[0].header('興趣')
    
    #
    cb = {}
    col1, col2, col3, col4 = st.columns(4)
    with col1:  
        cb['資訊'] = st.checkbox('資訊')
        cb['金融'] = st.checkbox('金融')
        cb['醫療'] = st.checkbox('醫療')
    with col2:
        cb['語文'] = st.checkbox('語文')
        cb['藝術'] = st.checkbox('藝術')
        cb['管理'] = st.checkbox('管理')
    with col3:
        cb['傳播'] = st.checkbox('傳播')
        cb['材料'] = st.checkbox('材料')
        cb['電通'] = st.checkbox('電通')
    with col4:
        cb['建築'] = st.checkbox('建築')
        cb['法政'] = st.checkbox('法政')
        cb['其他'] = st.checkbox('其他')
    #
    a, b, cols8, c, d = st.columns(5)
    submit = cols8.button('送出', use_container_width=True)
    if submit:
        interest_list = []
        for i in cb:
            if cb[i]:
                interest_list.append(i)
        info = {
            "chinese": chinese_score,
            "english": english_score,
            "mathA": mathA_score,
            "mathB": mathB_score,
            "science": science_score,
            "social": social_score,
            "listen": listen_score,
            "interest": interest_list
        }
        
        update_info(info)


def get_info():
    try:
        response = requests.get('http://127.0.0.1:8000/get_info')
        if response.status_code == 200:
            return response.json()
    except:
        st.warning('後臺程式未回應，請檢察後臺程式狀態')
        data = {'chinese': 0, 'english': 0, 'mathA': 0, 'mathB': 0, 
                    'science': 0, 'social': 0, 'listen': 'F', 'interest': []}
        return data

def update_info(info_data):
    try:
        response = requests.post('http://127.0.0.1:8000/update_info', data=json.dumps(info_data))
        if response.status_code == 200:
            st.success('修改成功')
        else:
            st.error('傳遞資訊有誤')
            st.text(json.dumps(info_data))
    except:
        st.warning('後臺程式未回應，請檢察後臺程式狀態')

if __name__ == '__main__':
    person_page()
