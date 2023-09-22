"""
归并排序：分治法思想
1、申请空间, 使其大小为两个已经排序序列之和, 该空间用来存放合并后的序列。
2、指定两个指针, 最初位置分别为两个已经排序序列的起始位置。
3、比较两个指针所指向的元素, 选择相对小的元素放入到合并空间, 并移动指针到下一位置; 
4、重复步骤3直到某一指针达到序列尾; 
5、将另一序列剩下的所有元素直接复制到合并序列尾。

时间复杂度: O(n log n)
空间复杂度: O(n)
"""
import typing


def MergeSort(arr: typing.List[int]):
    if len(arr) < 2:
        return arr
    middle = len(arr) // 2

    # 分解数据为小数据
    left, right = arr[0:middle], arr[middle:]
    return merge(MergeSort(left), MergeSort(right))


# 核心思想
def merge(left: typing.List[int], right: typing.List[int]):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


def merge1(left: typing.List[int], right: typing.List[int]):
    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


if __name__ == "__main__":
    nums = input("请输入一串数字,  数字之间空一个间隔：")
    arr = list(map(int, nums.rstrip().split()))
    result = MergeSort(arr)
    print("归并排序的结果为：", result)
