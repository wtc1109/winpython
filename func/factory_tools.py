import thread
import os
import time
import string

def python_cmd(cmd):
    #os.system(cmd)
    while True:
        str1 = "@%d"%(os.getpid())
        print cmd + str1
        os.system(cmd)
        #os.system("pause")
        time.sleep(10)

if __name__ == '__main__':
    pid = os.getpid()
    thread.start_new_thread(python_cmd, ("python newdevice_mssql.pyc",))
    thread.start_new_thread(python_cmd,("python -m CGIHTTPServer 8880",))
    while True:
        print os.getpid()
        time.sleep(100)