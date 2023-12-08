import subprocess
import time

# 定義 FastAPI 和 Streamlit 的命令
fastapi_command = "uvicorn API_server:app --reload"
streamlit_command = "streamlit run index.py"

# 使用 subprocess 開始 FastAPI 伺服器
fastapi_process = subprocess.Popen(fastapi_command, shell=True)
print('[*]FastAPI server started...')

# 等待一段時間，確保 FastAPI 伺服器已經成功啟動
time.sleep(2)

# 使用 subprocess 開始 Streamlit 應用
streamlit_process = subprocess.Popen(streamlit_command, shell=True)
print('[*]Streamlit app started...')

# 等待 Streamlit 應用退出，然後關閉 FastAPI 伺服器
streamlit_process.wait()
fastapi_process.terminate()
print('[*]Streamlit app closed...')