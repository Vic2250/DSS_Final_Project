import logging
import requests
import pandas as pd
import streamlit as st
from pathlib import Path
from pandas import DataFrame
import time
import re

#全域變數
subject_ranking = {}
department_list = []
distance_list = {}
school_list = []
interest = True

#獲取成績對應標?
try:
    response = requests.get('http://127.0.0.1:8000/get_subject_ranking')
    if response.status_code == 200:
        subject_ranking = response.json()
except:
    subject_ranking = {'國文': {'頂': 13, '前': 12, '均': 11, '後': 9, '底': 8}, 
                       '英文': {'頂': 13, '前': 11, '均': 8, '後': 5, ' 底': 4}, 
                       '數學A': {'頂': 11, '前': 9, '均': 7, '後': 5, '底': 4}, 
                       '數學B': {'頂': 12, '前': 10, '均': 7, '後': 4, '底': 3}, 
                       '社會': {'頂': 12, '前': 11, '均': 9, '後': 8, '底': 6}, 
                       '自然': {'頂': 13, '前': 11, '均': 9, '後': 6, '底': 5}}


class color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


def get_info():
    try:
        response = requests.get('http://127.0.0.1:8000/get_info')
        if response.status_code == 200:
            return response.json()
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


def read_path():
    file_path = Path("dataset/")
    excel_files = [file for file in file_path.iterdir() if file.suffix == '.xlsx']  # 取得所有xlsx檔案
    school_list = []
    info = pd.read_excel(excel_files[0])  # 讀取第一個Excel檔案
    for index, row in info.iloc[1:].iterrows():
        if row.iloc[1] not in school_list:
            school_list.append(row.iloc[1])
    return school_list


def analyze_page():
    global department_list, school_list, interest
    st.text('')
    st.text('')
    st.subheader('落點分析')
    st.text('')
    school_list = read_path()
    cols = st.columns([0.8, 0.2])
    with cols[0]:
        condition = st.multiselect('篩選條件', ['公立', '距離'], key='selection_condition')
    with cols[1]:
        all_list = st.checkbox('列出全部')
        interest = st.checkbox('興趣篩選',value=interest)
    if not all_list:
        selected_option = st.selectbox('學校', school_list, index=0)
    score = []
    interest_list = []
    # 獲取輸入的成績
    info_data = get_info()
    for key in info_data:
        if key != '興趣':
            score.append(info_data[key]['score'])
        else:
            for n in info_data['興趣']:
                interest_list.append(n)
    
    # 讀取檔案excel檔
    file_path = Path("dataset/")  # 替換成你的檔案路徑
    excel_files = list(file_path.glob("*.xlsx"))
    data = pd.read_excel(excel_files[0], keep_default_na=False)
    school_distance(data)
    
    #
    if not all_list:
        # 推薦的列表
        with st.spinner("請稍後..."):
            time.sleep(1)
            check_department(data, score, selected_option, interest_list) 
            sec_check(data, score, selected_option)
            selected_data = pd.DataFrame(
                {
                    "編號" : [i for i in range(1, len(department_list)+1)],
                    "學校" : department_list,
                }
            )
            cols = st.columns([0.00000001, 1])
            # 全部符合的列表
            with cols[1]:
                st.dataframe(selected_data, use_container_width=True, hide_index=True)
    else:
        expander_list = []
        school_list2 = []
        
        ###
        with st.spinner("請稍後..."):
            distance = "距離"
            public = "國立"
            if distance in condition:
                school_list2 = sorted(school_list, key=lambda x:distance_list[x])
                for school in school_list2:
                    check_department(data, score, school, interest_list)
                    sec_check(data, score, school)
                    new_expander = st.expander(school)
                    expander_list.append(new_expander)
            else:
                for school in school_list:
                    check_department(data, score, school, interest_list)
                    sec_check(data, score, school)
                    new_expander = st.expander(school)
                    expander_list.append(new_expander)
            
            if public in condition:
                pass
            ###
        
            for i, expander in enumerate(expander_list):
                check_department(data, score, school_list[i], interest_list)
                sec_check(data, score, school)
                with expander:
                    selected_data = pd.DataFrame(
                        {
                            "編號" : [i for i in range(1, len(department_list)+1)],
                            "學校" : department_list,
                        }
                    )
                    cols = st.columns([0.00000001, 1])
                    # 全部符合的列表
                    with cols[1]:
                        st.dataframe(selected_data, use_container_width=True, hide_index=True)
                
     

# 檢查科系是否通過門檻標準
def check_department(data: DataFrame , score: list, index: str, intere_list: list)->list:
    global department_list, distance_list
    department_list = []
    school = index
    for index, row in data.iloc[0:].iterrows():
        # 取得每一列的國、英、數A、數B、自、社、英聽資料
        col_school = row["學校"]
        col0 = row["科系"]
        col_depart = row["類別"]
        if col_school == school:
            if not check_threshold('國文', row['國'], score[0]):
                #print(color.RED, "[-]未通過 ", color.END, f'{col0}')
                continue 
            if not check_threshold('英文', row['英'], score[1]):
                #print(color.RED, "[-]未通過 ", color.END, f'{col0}')
                continue
            if not check_threshold('數學A', row['數A'], score[2]):
                #print(color.RED, "[-]未通過 ", color.END, f'{col0}')
                continue
            if not check_threshold('數學B', row['數B'], score[3]):
                #print(color.RED, "[-]未通過 ", color.END, f'{col0}')
                continue
            if not check_threshold('自然', row['自'], score[4]):
                #print(color.RED, "[-]未通過 ", color.END, f'{col0}')
                continue
            if not check_threshold('社會', row['社'], score[5]):
                #print(color.RED, "[-]未通過 ", color.END, f'{col0}')
                continue
            if not check_threshold('英聽', row['英聽'], score[6]):
                #print(color.RED, "[-]未通過 ", color.END, f'{col0}')
                continue
            
            if interest:
                if col_depart in intere_list:
                    department_list.append(col0)
            else:
                department_list.append(col0)
            #print(color.GREEN, "[+]通過   ", color.END, f'{col0}')
        else:
            continue
    return department_list


# 檢查文字內容並判斷是否超過標準
def check_threshold(subject: str, text: str, score: int)->bool:
    if text[0] == '-':
        return True
    elif text[0].isupper():
        if str(score) <= str(text[0]):
            return True
        else:
            return False
    else:
        weight = subject_ranking[subject][text[0]]
        if score >= weight:
            return True
        else:
            return False

###----###
def school_distance(data: DataFrame)->dict:
    global distance_list
    for index, row in data.iloc[1:].iterrows():
        # 取得每一列的國、英、數A、數B、自、社、英聽資料
        col_school = row["學校"]
        col_distance = row["距離"]
        
        distance_list[col_school] = int(col_distance)
    
    return distance_list

def sec_check(data: DataFrame, score: list, school: str) -> dict:
    global department_list
    a = ["國", "英", "數A", "數B", "自", "社"]
    pattern = re.compile(r'(' + '|'.join(a) + ')(?:\+(' + '|'.join(a) + '))*(?:=(\d+))?$')
    score_list = {}
    count = 0
    for i in a:
        score_list[i] = score[count]
        count+=1

    
    for index, row in data.iloc[0:].iterrows():
        
        ##
        filter = []
        filter.append(row["篩選一"])
        filter.append(row["篩選二"])
        filter.append(row["篩選三"])
        filter.append(row["篩選四"])
        filter.append(row["篩選五"])
        col_school = row["學校"]
        col_depart = row["科系"]
        if school == col_school:
            for n in filter:
                if n == "-":
                    break
                match1 = pattern.match(n)
                print(match1)
                if not sec_check_threshold(match1, score_list):
                    department_list.remove(col_depart)
                else:
                    pass
            
            
##
def sec_check_threshold(match1: re.Match, score: dict) -> bool:
    if match1 :
        matched_chars = match1.groups()[:-2]
        numbers = match1.groups()[-1]  
        ans = 0
        for i in matched_chars:  
            ans = ans + score[i]
        if ans < int(numbers):
            return False
        else:
            return True
            
    return
        
 
if __name__ == '__main__':
    analyze_page()
