"""
列出当前目录下的所有文件和目录名
"""
import os
print([d for d in os.listdir('.')])