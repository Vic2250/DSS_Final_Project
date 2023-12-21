import json
import random
import pandas as pd
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Dict


app = FastAPI()


class PersonInfo(BaseModel):
    chinese: int
    english: int
    mathA: int
    mathB: int
    science: int
    social: int
    listen: str
    interest: list


def get_standard():
    # 讀取Excel文件
    excel_file = 'standard.xlsx'
    data = pd.read_excel(excel_file, header=0)

    # 找出'112'列至第一個NaN的列數
    start_row = data[data['科目'] == 112].index[0]  # 找到'112'所在的行數
    end_row = data['科目'].isnull().idxmax()  # 找到第一個NaN所在的行數
    # 提取資料
    required_data = data.loc[start_row:end_row]  # 使用loc方法切片取出資料
    cols = required_data.columns.tolist()
    standard = {}

    i = 0
    while i < len(cols) - 2:
        result_dict = {}
        standard_values = required_data[cols[1]].tolist()
        subject_values = required_data[cols[i + 2]].tolist()
        for j in range(len(standard_values)):
            if standard_values[j] not in result_dict:
                result_dict[standard_values[j]] = {}
            result_dict[standard_values[j]] = subject_values[j]
        standard[cols[i + 2]] = result_dict
        i += 2
    standard.pop('數學', None)
    return(standard)


def trans_standard(info, standard):
    comparison = {'chinese': '國文', 'english':'英文', 'mathA': '數學A', 
                  'mathB': '數學B', 'science': '自然', 'social': '社會'}
    subject_standard = {}
    for key in info:
        if key in comparison:
            subject = standard[comparison[key]]
            if info[key] >= subject['底標']:
                if info[key] >= subject['後標']:
                    if info[key] >= subject['均標']:
                        if info[key] >= subject['前標']:
                            if info[key] >= subject['頂標']:
                                subject_standard[key] = '頂標'
                            else:
                                subject_standard[key] = '前標'
                        else:
                            subject_standard[key] = '均標'
                    else:
                        subject_standard[key] = '後標'
                else:
                    subject_standard[key] = '底標'
            else:
                subject_standard[key] = '底標'
    return subject_standard


@app.get('/get_info')
def get_info():
    try:
        with open('score.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        
        data = {
            "國文": {"score": 0, "rank": "Bottom"},
            "英文": {"score": 0, "rank": "Bottom"},
            "數A": {"score": 0, "rank": "Bottom"},
            "數B": {"score": 0,"rank": "Bottom"},
            "自然": {"score": 0,"rank": "Bottom"},
            "社會": {"score": 0,"rank": "Bottom"},
            "英聽": {"score": 3}}
       
        return data

@app.post('/update_info')
def update_info(info: PersonInfo):
    get_value = info.dict()
    standard = get_standard()
    subject_standard = trans_standard(get_value, standard)
    data = {
        '國文': {"score": get_value['chinese'], "rank": subject_standard['chinese']},
        '英文': {"score": get_value['english'], "rank": subject_standard['english']},
        '數A': {"score": get_value['mathA'], "rank": subject_standard['mathA']},
        '數B': {"score": get_value['mathB'], "rank": subject_standard['mathB']},
        '自然': {"score": get_value['science'], "rank": subject_standard['science']},
        '社會': {"score": get_value['social'], "rank": subject_standard['social']},
        '英聽': {"score": get_value['listen']}
    }
    with open('score.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("成功修改")
    return {"Message": "成功修改"}


@app.get('/get_subject_ranking')
def get_rank():
    standard = get_standard()
    # 將標籤名稱修改為更簡潔的形式 (頂標-> 頂 ...依此類推)
    updated_structure = {}
    for subject, scores in standard.items():
        updated_scores = {key.replace('標', ''): value for key, value in scores.items()}
        updated_structure[subject] = updated_scores
    return updated_structure