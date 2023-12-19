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
class listen_dict(BaseModel):
    score: str
    rank: str
class data(BaseModel):
    transportation: int
    info: Dict[str, Info]
    listen: listen_dict
    hope_department: str

all_score = {}

grading_criteria = {
    '國': {
        '底標': 0,
        '後標': 4,
        '均標': 5,
        '前標': 7,
        '頂標': 12
    },
    '英': {
        '底標': 0,
        '後標': 4,
        '均標': 5,
        '前標': 7,
        '頂標': 12
    },
    '數A': {
        '底標': 0,
        '後標': 4,
        '均標': 5,
        '前標': 7,
        '頂標': 12
    },
    '數B': {
        '底標': 0,
        '後標': 4,
        '均標': 5,
        '前標': 7,
        '頂標': 12
    },
    '自': {
        '底標': 0,
        '後標': 4,
        '均標': 5,
        '前標': 7,
        '頂標': 12
    },
    '社': {
        '底標': 0,
        '後標': 4,
        '均標': 5,
        '前標': 7,
        '頂標': 12
    },
}

@app.get('/showgraph')
def show_graph():
    global all_score
    
    df = pd.DataFrame(
        {
            "科目": ["國", "英", "數A", "數B", "自", "社", "英聽"],
            "分數": [str(all_score["info"]["國"]["score"]), str(all_score["info"]["英"]["score"]), str(all_score["info"]["數A"]["score"]), str(all_score["info"]["數B"]["score"]), str(all_score["info"]["自"]["score"]), str(all_score["info"]["社"]["score"]), all_score["listen"]["score"]],
            "等第": [all_score["info"]["國"]["rank"], all_score["info"]["英"]["rank"], all_score["info"]["數A"]["rank"], all_score["info"]["數B"]["rank"], all_score["info"]["自"]["rank"], all_score["info"]["社"]["rank"], all_score["listen"]["rank"]],
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
    with open('score.json', 'w') as file:
        file.write(item_json)
        
    return item_json

def compare_ranking(item_dict):
    for key, value in item_dict['info'].items():
        if value['score'] >= grading_criteria[key]['頂標']:
           item_dict['info'][key]['rank'] = '頂標'
        elif value['score'] >= grading_criteria[key]['前標']:
            item_dict['info'][key]['rank'] = '前標'
        elif value['score'] >= grading_criteria[key]['均標']:
            item_dict['info'][key]['rank'] = '均標'
        elif value['score'] >= grading_criteria[key]['後標']:
            item_dict['info'][key]['rank'] = '後標'
        else:
            item_dict['info'][key]['rank'] = '底標'
            
    if item_dict['listen']['score'] == 'A':
        item_dict['listen']['rank'] = '頂標'
    elif item_dict['listen']['score'] == 'B':
        item_dict['listen']['rank'] = '前標'
    elif item_dict['listen']['score'] == 'C':
        item_dict['listen']['rank'] = '均標'
    else:
        item_dict['listen']['rank'] = '後標'
    return item_dict


