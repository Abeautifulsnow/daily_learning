"""
插入排序：(稳定排序)
1、将第一待排序序列第一个元素看做一个有序序列，把第二个元素到最后一个元素当成是未排序序列。
2、从头到尾依次扫描未排序序列，将扫描到的每个元素插入到有序序列的适当位置。
（如果待插入的元素与有序序列中的某个元素相等，则将待插入元素插入到相等元素的后面）
缺点：效率低下，每次数据只能移动一位。
"""
def InsertionSort(arr):
    if len(arr) < 2:
        return arr
    for i in range(len(arr)):
        preIndex = i-1
        current = arr[i]
        while preIndex >= 0 and arr[preIndex] > current:
            arr[preIndex+1] = arr[preIndex]
            preIndex -= 1
        arr[preIndex+1] = current
    return arr


# 第二种插入排序算法
def insertion_sort1(data: list[int]) -> list[int]:
    if len(data) < 2:
        return data

    for i in range(0, len(data)):
        for j in range(i, 0, -1):
            if data[j - 1] > data[j]:
                data[j], data[j - 1] = data[j - 1], data[j]

    return data


if __name__ == "__main__":
    nums = input('请输入一串数字, 数字之间空一个间隔：')
    arr = list(map(int, nums.rstrip().split()))
    result = InsertionSort(arr)
    print('插入排序后的结果为：', result)
