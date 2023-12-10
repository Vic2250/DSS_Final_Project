import streamlit as st
import pandas as pd


def analyze_page():
    st.text('')
    st.text('')
    st.subheader('落點分析')
    st.text('')
    # 讀取xlsx檔案
    file_path = '001.xlsx'  # 請替換成你的檔案路徑

    # 使用pandas的read_excel方法讀取檔案
    data = pd.read_excel(file_path)
    # 顯示讀取的資料
    #print(data)

    # 印出所有國英數自社英聽
    # first_row = data.iloc[1:][['國', '英', '數A', '數B', '自', '社', '英聽']]
    # print(first_row)

    for index, row in data.iloc[1:].iterrows():
        # 取得每一列的國、英、數A、數B、自、社、英聽資料
        col0 = row['國立臺灣大學']
        col1 = row['國']
        col2 = row['英']
        col3 = row['數A']
        col4 = row['數B']
        col5 = row['自']
        col6 = row['社']
        col7 = row['英聽']

        # 在這裡進行每一列的比較或其他處理
        # 例如，進行條件比較或其他運算
        if col1 == '前3':
            # 做些什麼...
            print(f'符合條件的資料在索引 {col0}')
    # print(first_row)


if __name__ == '__main__':
    analyze_page()
