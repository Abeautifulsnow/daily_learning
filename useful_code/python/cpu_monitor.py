def load_stat():
    loadavg = {}
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    loadavg['lavg_1']=con[0]
    loadavg['lavg_5']=con[1]
    loadavg['lavg_15']=con[2]
    loadavg['nr']=con[3]


    prosess_list = loadavg['nr'].split('/')
    loadavg['running_prosess']=prosess_list[0]
    loadavg['total_prosess']=prosess_list[1]

    loadavg['last_pid']=con[4]

    return loadavg


if __name__ == "__main__":
    print(load_stat())
