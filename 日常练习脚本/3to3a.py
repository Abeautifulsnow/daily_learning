"""
替换列表中所有的3为3a
"""
num = ['harden', 'lampard', 3, 34, 45, 56, 76, 87, 78, 45, 3, 3, 3, 87686, 98, 76]
for i in range(num.count(3)):
    ele_index = num.index(3)
    print(ele_index)
    num[ele_index] = '3a'
print(num)
