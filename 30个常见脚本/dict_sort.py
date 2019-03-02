"""根据字典的值对字典进行排序"""
# import operator
# dict = {1:2, 3:4, 4:3, 2:1, 0:0}
# sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
# print(sorted_dict)

# 法二：lambda实现
dict = {1:2, 3:4, 4:3, 2:1, 0:0}
sorted_dict = sorted(dict.items(), key=lambda item: item[1])
print(sorted_dict)