L = [4, 1, 7, 4, 4, 6, 2, 1, 6, 6]

# 一
new_l = list(set(L))
new_l.sort(key=L.index)
print(new_l)

# 二
new_list = []
for m in L:
    if m not in new_list:
        new_list.append(m)

print(new_list)

# 三
new_list1 = []

for index, value in enumerate(L):
    if L.index(value) == index:
        new_list1.append(value)

print(new_list1)

# 四
new_ll = L[:]

for i in L:
    while new_ll.count(i) > 1:
        del new_ll[new_ll.index(i)]
new_ll.sort(key=L.index)
print(new_ll)

# 五
new_dict = dict.fromkeys(L)
L1 = list(new_dict.keys())
L1.sort(key=L.index)
print(L1)
