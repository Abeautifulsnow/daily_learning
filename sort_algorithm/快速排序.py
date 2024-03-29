"""
分治法思想
"""

from typing import List


# Complete the quickSort function below.
def quickSort(arr):
    if len(arr) < 2:
        return arr
    else:
        baseValue = arr[0]
        left, equal, right = [], [baseValue], []
        for m in arr[1:]:
            if m < baseValue:
                left.append(m)
            elif m > baseValue:
                right.append(m)
            else:
                equal.append(m)
        return quickSort(left) + equal + quickSort(right)


# method2: 挖坑法
def quickSort2(arr: List, left: int, right: int):
    if len(arr) < 2:
        return arr
    if left > right:
        return 0

    pivotNumber = arr[left]
    l = left
    r = right

    while l != r:
        while r > l and arr[r] >= pivotNumber:
            r -= 1
        if r > l:
            # 元素互换
            arr[l], arr[r] = arr[r], arr[l]

        while l < r and arr[l] <= pivotNumber:
            l += 1
        if l < r:
            # 元素互换
            arr[l], arr[r] = arr[r], arr[l]

    quickSort2(arr, left, l - 1)
    quickSort2(arr, l + 1, right)


# method3: 交换法
def quickSort3(arr: List, left: int, right: int):
    if len(arr) < 2:
        return arr
    if left > right:
        return 0

    pivotNumber = arr[left]
    l = left
    r = right

    while l != r:
        while r > l and arr[r] >= pivotNumber:
            r -= 1

        while l < r and arr[l] <= pivotNumber:
            l += 1
        if l < r:
            # 元素互换
            arr[l], arr[r] = arr[r], arr[l]

    # 元素互换
    arr[r], arr[left] = arr[left], arr[r]
    quickSort3(arr, left, l - 1)
    quickSort3(arr, l + 1, right)


# method4: 前后指针法
def quickSort4(arr: List, left: int, right: int):
    if left >= right or right > len(arr) - 1:
        return 0

    prev = left - 1
    cur = prev + 1
    key = right
    pivotNumber = arr[key]

    while cur != key:
        # 当cur小于最右值时，prev+1；判断cur和prev不同时候，交换
        # 当cur大于最右值时，prev不动，cur继续+1；prev还是之前的那个小于最右的数值，而cur已经比最右值大，且大于prev的值了
        # 当cur又比最右值小时候，判断prev和cur不等，执行交换
        if arr[cur] < pivotNumber:
            # 后移1位
            prev += 1

            if prev != cur:
                arr[prev], arr[cur] = arr[cur], arr[prev]
                print(arr)

        # cur也随着同时移动
        cur += 1

    prev += 1
    arr[prev], arr[key] = arr[key], arr[prev]
    quickSort4(arr, left, prev - 1)
    quickSort4(arr, prev + 1, right)


def quickSort5(alist: list, start: int, end: int):
    if start >= end:
        return

    pivot = alist[start]
    low = start
    high = end

    while low < high:
        # 比较最右侧的值与基准值的大小，如果大于基准值，就右指针往左侧移动
        # 直到右值小于基准值或右指针小于等于左指针，退出此轮循环
        while low < high and alist[high] >= pivot:
            high -= 1
        
        # 然后走到此位置时high指向一个比基准元素小的元素,将high指向的元素放到low的位置上,此时high指向的位置空着,接下来移动low找到符合条件的元素放在此处
        alist[low] = alist[high]

        # 比较最左侧的值与基准值的大小，如果小于基准值，就左指针往右侧移动
        # 直到左值大于等于基准值或左指针大于等于右指针，退出此轮循环
        while low < high and alist[low] < pivot:
            low += 1
        # 然后此时low指向一个比基准元素大的元素,将low指向的元素放到high空着的位置上,此时low指向的位置空着,之后进行下一次循环,将high找到符合条件的元素填到此处
        alist[high] = alist[low]

    # 退出循环后，low与high重合，此时所指位置为基准元素的正确位置,左边的元素都比基准元素小,右边的元素都比基准元素大
    # 将基准元素放到该位置
    alist[low] = pivot

    # 对基准元素左边的子序列进行快速排序
    quickSort5(alist, start, low - 1)

    # 对基准元素右边的子序列进行快速排序
    quickSort5(alist, low + 1, end)


if __name__ == "__main__":
    n = input("请输入一串数字, 数字之间空一个间隔：")
    arr = list(map(int, n.rstrip().split()))
    # result = quickSort(arr)
    result = arr
    quickSort4(result, 0, len(result) - 1)
    print("快排后的列表", result)
    print("将快排列表转换为字符串：", ",".join(map(str, result)))
