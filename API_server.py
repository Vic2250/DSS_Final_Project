import random
import json
import pandas as pd
from fastapi import FastAPI, Response


app = FastAPI()


@app.get('/test')
def show_graph():
    df = pd.DataFrame(
        {
            "科目": ["國", "英", "數A", "數B", "自", "社"],
            "分數": [random.randint(0, 15) for _ in range(6)],
            "等第": [random.choice(["底標", "後標", "均標", "前標", "頂標"]) for _ in range(6)]
        }
    )
    # 將 DataFrame 轉換為 JSON 格式
    json_response = json.dumps(df.to_dict(orient="records"))

    # 返回 JSON 格式的數據
    return json_response
