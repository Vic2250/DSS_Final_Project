# DSS Final Project (落點分析系統)

### 作業環境

 1. Anaconda: https://www.anaconda.com/
 2. Python version: 3.10.13

### 執行步驟
 1. 開啟兩個Terminal

 2. 安裝套件
 ```python
 pip install -r requirements.txt
 ```
 3. Terminal1: 啟動後台
 ```python
 uvicorn API_server:app
 ```

 4. Terminal2" 啟動UI
 ```python
 streamlit run index.py
 ```