"""
选择排序：
1、首先在未排序的序列中找到最小或者最大的元素，放在排序序列的起始位置。
2、然后再从未排序元素中继续找寻最小或者最大的元素，然后放到已排序序列的末尾。
3、重复上面第二步，直到所有元素排序完毕。
"""


def selection_sort(arr):
    for i in range(len(arr) - 1):
        # 先 记录一个最小数的索引
        minIndex = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minIndex]:
                # i不是最小数时，将最小数与i进行交换
                minIndex = j
        if i != minIndex:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr


if __name__ == "__main__":
    nums = input("请输入一串数字, 数字之间空一个间隔：")
    arr = list(map(int, nums.rstrip().split()))
    result = selection_sort(arr)
    print("选择排序的结果为：", result)
