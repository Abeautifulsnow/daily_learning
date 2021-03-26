"""将符号变成空格"""
# 方法一：
# str1 = '你好$$$我正在学Python@#@#现在需要&*&*&修改字符串'
# new_str = str1.replace('$$$', ' ').replace('@#@#', ' ').replace('&*&*&', ' ')
# print(new_str)

# 方法二
import re

str1 = '你好$$$我正在学Python@#@#现在需要&*&*&修改字符串'
new_str = re.sub('[@#$&*]+', ' ', str1)
print(new_str)
