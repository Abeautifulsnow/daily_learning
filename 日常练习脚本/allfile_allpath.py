"""
输出某个路径下的所有文件和文件夹的路径
"""
import os


def print_dir():
    file_path = input("请输入一个路径：")
    if file_path == "":
        print("请输入正确的路径")
    else:
        # 获取目录中的文件及子目录列表
        for i in os.listdir(file_path):
            print(os.path.join(file_path, i))


def show_dir(file_path):
    for i in os.listdir(file_path):
        path = (os.path.join(file_path, i))
        print(path)
        if os.path.isdir(path):
            show_dir(path)


print([d for d in os.listdir('.')])
