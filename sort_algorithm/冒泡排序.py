"""
冒泡排序：（稳定排序）
冒泡排序是一种简单的排序算法，一次比较两个值，如果他们的顺序错误，就给交换过来
"""


def bubble_sort(arr):
    for i in range(1, len(arr)):  # 这个循环负责设置冒泡排序进行的次数
        for j in range(0, len(arr) - i):  # j为列表下标
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def short_bubble_sort(arr):
    exchanges = True
    passnum = len(arr) - 1

    while passnum > 0 and exchanges:
        exchanges = False

        for i in range(passnum):
            if arr[i] > arr[i + 1]:
                exchanges = True
                print(passnum)
                arr[i], arr[i + 1] = arr[i + 1], arr[i]

        passnum -= 1

    return arr


if __name__ == "__main__":
    nums = input("请输入一串数字, 数字之间空一个间隔：")
    arr = list(map(int, nums.rstrip().split()))
    # result = bubble_sort(arr)
    result = short_bubble_sort(arr)
    print("冒泡排序的结果为：", result)
