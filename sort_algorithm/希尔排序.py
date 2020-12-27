"""
希尔排序：非稳定排序
又称递减增量排序算法。
1、选择一个增量序列t1，t2,...，tk，其中ti>tj，tk=1；
2、按增量序列个数k，对序列进行k趟排序；
3、每趟排序，根据对应的增量ti，将待排序列分割成若干长度为m的子序列，分别对各子表进行直接插入排序。
仅增量因子为1时，整个序列作为一个表来处理，表长度即为整个序列的长度。
"""
def shellsort(arr):
    import math
    gap = 1
    while (gap < len(arr)/3):
        gap = gap*3 + 1
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i - gap
            while j >= 0 and arr[j] > temp:
                arr[j+gap] = arr[j]
                j -= gap
            arr[j+gap] = temp
        gap = math.floor(gap/3)
    return arr


if __name__ == "__main__":
    nums = input('请输入一串数字, 数字之间空一个间隔：')
    arr = list(map(int, nums.rstrip().split()))
    result = shellsort(arr)
    print('希尔排序后的结果为：', result)
