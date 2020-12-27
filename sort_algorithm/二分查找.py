"""
二分查找:必须为有序存储结构
"""

# 法一：非递归
def binary_search(data, sort_arr):
    low = 0
    high = len(sort_arr) - 1
    while low <= high:
        mid = int((high + low) / 2)
        if sort_arr[mid] == data:
            return mid
        elif data < sort_arr[mid]:
            high = mid - 1
        elif data > sort_arr[mid]:
            low = mid + 1
    return '找不到{}这个值...'.format(data)


sort_arr = [1, 5, 6, 7, 9, 15, 27, 38, 49, 50, 53]
index = binary_search(15, sort_arr)
if isinstance(index, str):
    print(index)
else:
    print('查找的索引是{0}，对应的数字是{1}'.format(index, sort_arr[index]))


# 法二：递归法
# def binary_search(sort_arr,aim,start = 0,end = None):
#     end = len(sort_arr) if end is None else end
#     mid_index = (end - start) // 2 + start
#     if start <= end:
#         if sort_arr[mid_index] < aim:
#             return binary_search(sort_arr,aim,start = mid_index+1,end=end)
#         elif sort_arr[mid_index] > aim:
#             return binary_search(sort_arr,aim,start=start,end=mid_index-1)
#         else:
#             return mid_index
#     else:
#         return '找不到{}这个值...'.format(aim)


# if __name__ == '__main__':
#     sort_arr = [1, 5, 6, 7, 9, 15, 27, 38, 49, 50]
#     index = binary_search(sort_arr, 39)
#     if isinstance(index, str):
#         print(index)
#     else:
#         print('查找的索引是{0}，对应的数字是{1}'.format(index, sort_arr[index]))