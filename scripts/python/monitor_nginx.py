import os, sys, time


while True:
    print("==============检测nginx是否正在运行===============")
    time.sleep(4)
    try:
        ret = os.popen('ps -C nginx -o pid,cmd').readlines()
        if len(ret) < 2:
            print("nginx进程异常退出，4秒后重启")
            time.sleep(3)
            os.system('service nginx restart')
            print("nginx正在重启")
        else:
            print("nginx正在运行当中...")
            break
    except:
        print("Error", sys.exc_info())
