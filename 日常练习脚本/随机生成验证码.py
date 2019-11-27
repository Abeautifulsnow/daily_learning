"""
import random

list1 = []

for i in range(65, 91):
    list1.append(chr(i))    # chr将65-90Ascii码转换为Unicode统一码A-Z
for j in range(97, 123):
    list1.append(chr(j))    # chr将97-122Ascii码转换为Unicode统一码a-z
for k in range(48, 58):
    list1.append(chr(k))    # chr将48-57Ascii码转换为Unicode统一码0-9

ma = random.sample(list1, 6)
print(ma)
ma = ''.join(ma)
print(ma)
"""

# 法二：
import random, string

str1 = string.digits
str2 = string.ascii_letters
str3 = str1 + str2
ma1 = random.sample(str3, 6)
ma1 = ''.join(ma1)
print(ma1)
