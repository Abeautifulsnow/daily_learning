#!/bin/python3
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

if __name__ == "__main__":
    n = input('请输入一串数字, 数字之间空一个间隔：')
    arr = list(map(int, n.rstrip().split()))
    result = quickSort(arr)
    print("快排后的列表", result)
    print("将快排列表转换为字符串：", ','.join(map(str, result)))
