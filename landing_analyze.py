import streamlit as st
import pandas as pd
import os
import requests
import json
import logging

class color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

def score_weight(word):
    if word == '底':
        return 0
    elif word == '後':
        return 4
    elif word == '均':
        return 5
    elif word == '前':
        return 7
    elif word == '頂':
        return 12


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
    file_path = 'info/'  # 請替換成你的檔案路徑
    excel_files = read_excel_files_in_folder(file_path)
    # 使用pandas的read_excel方法讀取檔案
    
    data = pd.read_excel(excel_files[0])
    # 顯示讀取的資料
    #print(data)

    # 印出所有國英數自社英聽
    # first_row = data.iloc[1:][['國', '英', '數A', '數B', '自', '社', '英聽']]
    # print(first_row)

    # 測試用使用者的數據[國、英、數A、數B、]
    #test = [4, 5, 3, 4, 5, 4, 'B']
    test = []
    with open('score.json', 'r') as file:
        score_data = json.load(file)
    
    info_data = score_data['info']
    for key, value in info_data.items():
        test.append(value['score'])
    test.append(score_data['listen']['score'])
 
    for index, row in data.iloc[1:].iterrows():
        # 取得每一列的國、英、數A、數B、自、社、英聽資料
        col0 = row['國立臺灣大學']
        col1 = row['國']
        if not check_threshold(col1, test[0]):
            print(color.RED, "[-]未通過 ", color.END, f'{col0}')
            continue
        col2 = row['英']
        if not check_threshold(col2, test[1]):
            print(color.RED, "[-]未通過 ", color.END, f'{col0}')
            continue
        col3 = row['數A']
        if not check_threshold(col3, test[2]):
            print(color.RED, "[-]未通過 ", color.END, f'{col0}')
            continue
        col4 = row['數B']
        if not check_threshold(col4, test[3]):
            print(color.RED, "[-]未通過 ", color.END, f'{col0}')
            continue
        col5 = row['自']
        if not check_threshold(col5, test[4]):
            print(color.RED, "[-]未通過 ", color.END, f'{col0}')
            continue
        col6 = row['社']
        if not check_threshold(col6, test[5]):
            print(color.RED, "[-]未通過 ", color.END, f'{col0}')
            continue
        col7 = row['英聽']
        if not check_threshold(col7, test[6]):
            print(color.RED, "[-]未通過 ", color.END, f'{col0}')
            continue
        print(color.GREEN, "[+]通過 ", color.END, f'{col0}')


def read_excel_files_in_folder(folder_path):
    excel_files = []
    
    if not os.path.exists(folder_path):
        print(f"資料夾 '{folder_path}' 不存在。")
        return excel_files

    files = os.listdir(folder_path)

    for file in files:
        if file.endswith(".xlsx") or file.endswith(".xls"):
            excel_files.append(os.path.join(folder_path, file))

    return excel_files

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    analyze_page()
