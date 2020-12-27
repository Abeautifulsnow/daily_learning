"""
归并排序：
1、申请空间，使其大小为两个已经排序序列之和，该空间用来存放合并后的序列。
2、指定两个指针，最初位置分别为两个已经排序序列的起始位置。
3、比较两个指针所指向的元素，选择相对小的元素放入到合并空间，并移动指针到下一位置；
4、重复步骤3直到某一指针达到序列尾；
5、将另一序列剩下的所有元素直接复制到合并序列尾。
"""
def MergeSort(arr):
    import math
    if(len(arr) < 2):
        return arr
    middle = math.floor(len(arr)/2)
    left, right = arr[0:middle], arr[middle:]
    return merge(MergeSort(left), MergeSort(right))

def merge(left, right):
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


if __name__ == "__main__":
    nums = input('请输入一串数字, 数字之间空一个间隔：')
    arr = list(map(int, nums.rstrip().split()))
    result = MergeSort(arr)
    print('归并排序的结果为：', result)
