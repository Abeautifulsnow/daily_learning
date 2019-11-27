'''
输出某个路径下的所有文件和文件夹的路径
'''
import os

def show_dir(filepath):
    for i in os.listdir(filepath):
        path = (os.path.join(filepath, i))
        print(path)
        if os.path.isdir(path):
            show_dir(path)

filepath = '/home/django/My_python'
show_dir(filepath)