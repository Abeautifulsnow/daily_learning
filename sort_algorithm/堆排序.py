"""
堆排序：

"""


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # 主要是比较出 left - root - right 谁最大, 并最终将最大的值赋给root
    # 比较root和左节点大小, 如果左节点大, 就将largest指针赋值为左节点
    if l < n and arr[i] < arr[l]:
        largest = l

    # 然后比较最大值和右节点比较, 如果右节点大, 就将largest指针赋值为右节点
    if r < n and arr[largest] < arr[r]:
        largest = r

    # 以上两步骤, 主要是拿出最大堆的root值
    # 如果最大值和root的指针不相等, 就将最大值和root互换位置
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # 交换最大值和root

        # 当前largest指针所代表的值并不是最大值【已发生过交换】, 然后再去比较largest的二叉树
        heapify(arr, n, largest)


def heap_sort(arr: list):
    n = len(arr)
    if n < 2:
        return arr
    else:
        # Build a maxheap.构建最大堆
        for i in range(n, -1, -1):
            heapify(arr, n, i)

        # 然后逐个和0去做比较并交换
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # 交换
            heapify(arr, i, 0)
