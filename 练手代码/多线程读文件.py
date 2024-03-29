import pathlib
import sys
import threading


class Reader(threading.Thread):
    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def run(self):
        while True:
            with mutex:
                line = fp.readline()
                if len(line) == 0:
                    return
                print('%d:%s' % (self.num, line), end='')
        fp.close()


def get_input_params() -> Tuple[str, int]:
    global file, threadNums
    if len(sys.argv) == 1:
        raise SystemError("请输入参数, 您可以输入-h查看用法.")
    if len(sys.argv) == 2:
        param1 = sys.argv[1]
        if param1 in ('-h', '--h', 'help', '--help'):
            print(f"用法: python {sys.argv[0]} [file_path] [thread_nums]")
            print("Note: file_path 必填参数, thread_nums为选填参数, 默认值为5.")
            exit(0)
        else:
            file = param1
            if not pathlib.Path(file).exists():
                raise FileNotFoundError("文件不存在, 请检查输入参数.")
        # 设置线程数模认值为5
        threadNums = 5

    if len(sys.argv) == 3:
        file = sys.argv[1]
        if not pathlib.Path(file).exists():
            raise FileNotFoundError("文件不存在, 请检查输入参数.")
        threadNums = int(sys.argv[2])
    
    return file, threadNums


if __name__ == '__main__':
    file, threadNums = get_input_params()
    fp = open(file)
    mutex = threading.Lock()

    t_jobs = []
    for i in range(threadNums):
        ti = Reader(i)
        t_jobs.append(ti)
        ti.start()
    
    for t in t_jobs:
        t.join()
