'''
输出某个路径及其子目录下的所有以.html为后缀的文件
'''
import os

def print_dir(filepath):
    for i in os.listdir(filepath):
        path = os.path.join(filepath, i)
        if os.path.isdir(path):
            print_dir(path)
        if path.endswith(".html"):
            print(path)

filepath = '/home/django/My_python'
print_dir(filepath)