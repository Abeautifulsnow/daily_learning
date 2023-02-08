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


if __name__ == "__main__":
    n = input("请输入一串数字, 数字之间空一个间隔：")
    arr = list(map(int, n.rstrip().split()))
    # result = quickSort(arr)
    result = arr
    quickSort4(result, 0, len(result) - 1)
    print("快排后的列表", result)
    print("将快排列表转换为字符串：", ",".join(map(str, result)))
