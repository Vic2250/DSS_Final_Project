import requests
import json
import streamlit as st
import pandas as pd


def ranking_page():
    st.text('')
    st.text('')
    st.subheader('各科級距')
    st.text('')
    response = requests.get("http://127.0.0.1:8000/showgraph").json()
    data = json.loads(response)
    #print(response)
    df = pd.DataFrame(data)
    cols = st.columns([0.1, 0.7, 0.2])
    with cols[1]:
        st.dataframe(df, use_container_width=True, hide_index=True)
    

if __name__ == '__main__':
    ranking_page()
