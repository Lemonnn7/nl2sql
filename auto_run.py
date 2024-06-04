import psutil
import subprocess
import time
pid_lst = []
def kill_previous_process():
    for proc in psutil.process_iter():
        # print(proc.cmdline())
        try:
            # 查找名为 python.exe 的进程，并且命令行包含 test.py
            if "python.exe" in proc.name() and str(proc.pid) in pid_lst:
                proc.terminate()  # 终止进程
                print("删掉进程,id为{}".format(proc.pid))
                pid_lst.remove(str(proc.pid))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def start_new_process():
    process = subprocess.Popen(["D:\Miniforge3\envs\llm\python", "test.py"])  # 启动新的 Python 进程
    pid_lst.append(str(process.pid))
    print("进程已经重启,id为{}".format(process.pid))

if __name__ == "__main__":
    while True:
        kill_previous_process()  # 杀死之前的进程
        start_new_process()  # 启动新的进程
        time.sleep(60)  # 每小时重复