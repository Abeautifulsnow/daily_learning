"""
输出某个路径及其子目录下的所有以.html为后缀的文件
"""
import os


def print_dir(file_path):
    for i in os.listdir(file_path):
        path = os.path.join(file_path, i)
        if os.path.isdir(path):
            print_dir(path)
        if path.endswith(".html"):
            print(path)


filepath = '/home/django/My_python'
print_dir(filepath)
