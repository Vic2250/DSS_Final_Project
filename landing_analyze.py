import streamlit as st
import pandas as pd
from pandas import DataFrame
import os
import requests
import json
import logging

department_list = []
school_list = []
excel_files = []
file_path = 'dataset/'  # 請替換成你的檔案路徑
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

def check_department(data: DataFrame , test: list, index: str):
    global department_list
    global school_list
    department_list = []
    school = index
    #print(school)
    for index, row in data.iloc[1:].iterrows():
        # 取得每一列的國、英、數A、數B、自、社、英聽資料
        col_school = row["學校"]
        col0 = row["科系"]
        col1 = row['國']
        if col_school == school:
            if col1 == '':
                break
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
            department_list.append(col0)
            print(color.GREEN, "[+]通過 ", color.END, f'{col0}')
        else:
            continue

    return department_list

def analyze_page():
    global school_list
    global excel_files
    global department_list
    global file_path
    
    logging.basicConfig(level=logging.INFO)
    read_path()
    
    st.text('')
    st.text('')
    st.subheader('落點分析')
    st.text('')
    
    #data = pd.read_excel(file_path + excel_files[0])
   
    #test = [4, 5, 3, 4, 5, 4, 'B']
    test = []
    with open('score.json', 'r') as file:
        score_data = json.load(file)
    
    info_data = score_data['info']
    for key, value in info_data.items():
        test.append(value['score'])
    test.append(score_data['listen']['score'])
    
    #print(test)
    # 選擇框中的選項
    selected_option = st.selectbox('學校', school_list, index=0)
    
    #print(file_path + excel_files[index])
    data = pd.read_excel(file_path + excel_files[0], keep_default_na=False)
    check_department(data, test, selected_option)   
    # 根據選擇的選項生成相應的表格
    selected_data = pd.DataFrame(
        {
            "編號" : [i for i in range(1, len(department_list)+1)],
            "學校" : department_list,
        }
    )
    cols = st.columns([0.2, 1])
    with cols[1]:
        st.dataframe(selected_data, use_container_width=True, hide_index=True)
    #st.write(selected_data)
    

def read_excel_files_in_folder(folder_path):
   
    return excel_files

#新版dataset
def read_path():
    global school_list
    global excel_files
    file_path =  "dataset/"  # 請替換成你的檔案路徑
    excel_files = os.listdir(file_path)
    print(excel_files)
    school_list = []
    info = pd.read_excel(file_path + excel_files[0])
    for index, row in info.iloc[1:].iterrows():
        if row.iloc[1] not in school_list:
            school_list.append(row.iloc[1])

#舊版info
"""
def read_path():
    global excel_files
    global school_list
    file_path = 'info/'  # 請替換成你的檔案路徑
    excel_files = os.listdir(file_path)
    # 使用pandas的read_excel方法讀取檔案
    #print(excel_files)
    school_list = []
    for file in excel_files:
        if file.endswith(".xlsx") or file.endswith(".xls"):
            if file.startswith("j"):
                info = pd.read_excel(file_path + file)
                v2 = info.keys()[2]
                school_list.append(v2)
            else:
                info = pd.read_excel(file_path + file)
                v2 = info.keys()[1]
                school_list.append(v2)
    #print(school_list)
    """

if __name__ == '__main__':
    analyze_page()
