import streamlit as st
import pandas as pd


def score_weight(word):
    if word == '底':
        return 1
    elif word == '後':
        return 2
    elif word == '均':
        return 3
    elif word == '前':
        return 4
    elif word == '頂':
        return 5


def check_threshold(text, score):
    if text[0] == '-':
        return True
    elif text[0].isupper():
        if score <= text[0]:
            return True
        else:
            return False
    else:
        weight = score_weight(text[0])
        if score >= weight:
            return True
        else:
            return False


def analyze_page():
    st.text('')
    st.text('')
    st.subheader('落點分析')
    st.text('')
    # 讀取xlsx檔案
    file_path = 'info/001.xlsx'  # 請替換成你的檔案路徑

    # 使用pandas的read_excel方法讀取檔案
    data = pd.read_excel(file_path)
    # 顯示讀取的資料
    #print(data)

    # 印出所有國英數自社英聽
    # first_row = data.iloc[1:][['國', '英', '數A', '數B', '自', '社', '英聽']]
    # print(first_row)

    # 測試用使用者的數據[國、英、數A、數B、]
    test = [4, 5, 3, 4, 5, 4, 'B']

    for index, row in data.iloc[1:].iterrows():
        # 取得每一列的國、英、數A、數B、自、社、英聽資料
        col0 = row['國立臺灣大學']
        col1 = row['國']
        if not check_threshold(col1, test[0]):
            print(f'{col0} 未通過')
            continue
        col2 = row['英']
        if not check_threshold(col2, test[1]):
            print(f'{col0} 未通過')
            continue
        col3 = row['數A']
        if not check_threshold(col3, test[2]):
            print(f'{col0} 未通過')
            continue
        col4 = row['數B']
        if not check_threshold(col4, test[3]):
            print(f'{col0} 未通過')
            continue
        col5 = row['自']
        if not check_threshold(col5, test[4]):
            print(f'{col0} 未通過')
            continue
        col6 = row['社']
        if not check_threshold(col6, test[5]):
            print(f'{col0} 未通過')
            continue
        col7 = row['英聽']
        if not check_threshold(col7, test[6]):
            print(f'{col0} 未通過')
            continue
        print(f'恭喜 {col0} 通過')


if __name__ == '__main__':
    analyze_page()
