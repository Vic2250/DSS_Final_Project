import subprocess
import threading
import time

class color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

# 定義 FastAPI 和 Streamlit 的命令
fastapi_command = "uvicorn API_server:app --reload"
streamlit_command = "streamlit run index.py"

def start_fastapi():
    fastapi_process = subprocess.Popen(fastapi_command, shell=True)
    fastapi_process.wait()

def start_streamlit():
    streamlit_process = subprocess.Popen(streamlit_command, shell=True)
    streamlit_process.wait()

# 使用 threading 開始 FastAPI 和 Streamlit
fastapi_thread = threading.Thread(target=start_fastapi)
streamlit_thread = threading.Thread(target=start_streamlit)

# 開始 FastAPI 伺服器
fastapi_thread.start()
print(color.GREEN + '[*]FastAPI server started...' + color.END)

# 等待一段時間，確保 FastAPI 伺服器已經成功啟動
time.sleep(2)

# 開始 Streamlit 應用
streamlit_thread.start()
print(color.GREEN + '[*]Streamlit app started...' + color.END)

try:
    # 等待 Streamlit 應用退出
    streamlit_thread.join()
except KeyboardInterrupt:
    print(color.RED + '[*]Stopping FastAPI server...' + color.END)
    fastapi_thread.join()
    fastapi_thread._stop()
    
try:
    # 等待 FastAPI 伺服器退出
    fastapi_thread.join()
except KeyboardInterrupt:
    print(color.RED + '[*]Stopping Streamlit app...' + color.END)
    streamlit_thread.join()
    streamlit_thread._stop()
    
