import os


list1 = []
sum = 0
str1 = os.popen('ps aux', 'r').readlines()
for i in str1:
    str2 = i.split()
    new_rss = str2[5]
    list1.append(new_rss)

# 包含index=1到index=-2区间的元素
for m in list1[1:-1]:
    num = int(m)
    sum += num


print(list1)
print(f"{list1[0]}:{sum}")
# print(sorted(list, reverse=True))