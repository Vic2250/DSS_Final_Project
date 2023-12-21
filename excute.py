import asyncio
import subprocess
import threading
im

class color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

# 定義 FastAPI 和 Streamlit 的命令
fastapi_command = "uvicorn API_server:app --reload"
streamlit_command = "streamlit run index.py"

async def start_fastapi():
    fastapi_process = await asyncio.create_subprocess_shell(fastapi_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await fastapi_process.communicate()

async def start_streamlit():
    streamlit_process = await asyncio.create_subprocess_shell(streamlit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await streamlit_process.communicate()

# 开始 FastAPI 和 Streamlit
loop = asyncio.get_event_loop()
fastapi_task = loop.create_task(start_fastapi())
streamlit_task = loop.create_task(start_streamlit())

print(color.GREEN + '[*]FastAPI server and Streamlit app started...' + color.END)

try:
    loop.run_until_complete(asyncio.gather(fastapi_task, streamlit_task))
except KeyboardInterrupt:
    print(color.RED + '[*]Stopping FastAPI server and Streamlit app...' + color.END)
    loop.run_until_complete(asyncio.gather(fastapi_task, streamlit_task))
    loop.stop()
    loop.close()
