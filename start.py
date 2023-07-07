import subprocess
import time

def start_fastapi_server():
    subprocess.Popen(['uvicorn', 'main:app', '--reload'])

def start_gui_application():
    subprocess.Popen(['python', 'gui.py'])

if __name__ == "__main__":
    start_fastapi_server()
   
    time.sleep(5)
    start_gui_application()
