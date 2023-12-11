import json
import random

import pandas as pd
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Info(BaseModel):
    score: int
    rank: str

class data(BaseModel):
    transportation: str
    info: Dict[str, Info]
    hope_department: str

all_score = {}

grading_criteria = {
    '國': {
        '後標': {'min': 4, 'max': 5},
        '均標': {'min': 5, 'max': 7},
        '前標': {'min': 7, 'max': 12},
        '頂標': {'min': 12, 'max': 15}
    },
    '英': {
        '後標': {'min': 4, 'max': 5},
        '均標': {'min': 5, 'max': 7},
        '前標': {'min': 7, 'max': 12},
        '頂標': {'min': 12, 'max': 15}
    },
    '數A': {
        '後標': {'min': 4, 'max': 5},
        '均標': {'min': 5, 'max': 7},
        '前標': {'min': 7, 'max': 12},
        '頂標': {'min': 12, 'max': 15}
    },
    '數B': {
        '後標': {'min': 4, 'max': 5},
        '均標': {'min': 5, 'max': 7},
        '前標': {'min': 7, 'max': 12},
        '頂標': {'min': 12, 'max': 15}
    },
    '自': {
        '後標': {'min': 4, 'max': 5},
        '均標': {'min': 5, 'max': 7},
        '前標': {'min': 7, 'max': 12},
        '頂標': {'min': 12, 'max': 15}
    },
    '社': {
        '後標': {'min': 4, 'max': 5},
        '均標': {'min': 5, 'max': 7},
        '前標': {'min': 7, 'max': 12},
        '頂標': {'min': 12, 'max': 15}
    },
}

@app.get('/showgraph')
def show_graph():
    global all_score
    scores_list = []
    
    df = pd.DataFrame(
        {
            "科目": ["國", "英", "數A", "數B", "自", "社"],
            "分數": [all_score["info"]["國"]["score"], all_score["info"]["英"]["score"], all_score["info"]["數A"]["score"], all_score["info"]["數B"]["score"], all_score["info"]["自"]["score"], all_score["info"]["社"]["score"]],
            "等第": [all_score["info"]["國"]["rank"], all_score["info"]["英"]["rank"], all_score["info"]["數A"]["rank"], all_score["info"]["數B"]["rank"], all_score["info"]["自"]["rank"], all_score["info"]["社"]["rank"]]
        }
    )
    # 將 DataFrame 轉換為 JSON 格式
    json_response = json.dumps(df.to_dict(orient="records"))
 
    # 返回 JSON 格式的數據
    return json_response



@app.post('/getdata')
def get_data(item: data):
    global all_score
    request = item.dict()
    
    #比對等第
    item_dict = compare_ranking(request)
    all_score = item_dict.copy()
    
    # 將字典轉換成 JSON 字串
    item_json = return_to_json(item_dict)
    return item_json


def return_to_json(item_dict):
    
    item_json = json.dumps(item_dict, ensure_ascii=False)
    
    #print(item_json)
    with open('socre.json', 'w') as file:
        file.write(item_json)
        
    return item_json

def compare_ranking(item_dict):
    for key, value in item_dict['info'].items():
        if value['score'] >= grading_criteria[key]['頂標']['min']:
            item_dict['info'][key]['rank'] = '頂標'
        elif value['score'] >= grading_criteria[key]['前標']['min']:
            item_dict['info'][key]['rank'] = '前標'
        elif value['score'] >= grading_criteria[key]['均標']['min']:
            item_dict['info'][key]['rank'] = '均標'
        elif value['score'] >= grading_criteria[key]['後標']['min']:
            item_dict['info'][key]['rank'] = '後標'
        else:
            item_dict['info'][key]['rank'] = '底標'
            
    return item_dict


