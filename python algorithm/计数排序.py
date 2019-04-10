"""
计数排序：
计数排序的核心在于将输入的数据值转化为键存储在额外开辟的数组空间中。
作为一种线性时间复杂度的排序，计数排序要求输入的数据必须是有确实范围的整数。
"""
def countingSort(arr, maxValue):
    bucketLen = maxValue + 1
    bucket = [0]*bucketLen
    sortedIndex = 0
    arrLen = len(arr)
    for i in range(arrLen):
        if not bucket[arr[i]]:
            bucket[arr[i]] = 0
        bucket[arr[i]] += 1
    for j in range(bucketLen):
        while bucket[j] > 0:
            arr[sortedIndex] = j
            sortedIndex += 1
            bucket[j] -= 1
    return arr


if __name__ == "__main__":
    nums = input('请输入一串数字, 数字之间空一个间隔：')
    arr = list(map(int, nums.rstrip().split()))
    result = countingSort(arr, 10)
    print('计数排序的结果为：', result)
