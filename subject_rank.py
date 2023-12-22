import requests
import pandas as pd
import streamlit as st


def ranking_page():
    # 級距分布
    st.text('')
    st.text('')
    st.subheader('各科級距')
    st.text('')
    data = get_info()
    del data['興趣']
    df = pd.DataFrame(data).T.reset_index()
    df.columns = ['科目', '分數', '等第']  # 設置欄位名稱
    cols = st.columns([0.1, 0.7, 0.2])
    with cols[1]:
        st.table(df)
        #st.dataframe(df, use_container_width=True, hide_index=True)
    # 如果可以的話可以產一個可圖表(有關於分數或是級距的圖表(但不知道如何畫以及要畫成怎樣))


def get_info() -> dict:
    try:
        response = requests.get('http://127.0.0.1:8000/get_info')
        if response.status_code == 200:
            return response.json()
        if response == None:
            st.error("請送出資料")
    except:
        st.warning('後臺程式未回應，請檢察後臺程式狀態')
        data = {
            "國文": {"score": 0,"rank": "底標"},
            "英文": {"score": 0,"rank": "底標"},
            "數A": {"score": 0,"rank": "底標"},
            "數B": {"score": 0,"rank": "底標"},
            "自然": {"score": 0,"rank": "底標"},
            "社會": {"score": 0,"rank": "底標"},
            "英聽": {"score": "F"}
            }
        return data


if __name__ == '__main__':
    ranking_page()
