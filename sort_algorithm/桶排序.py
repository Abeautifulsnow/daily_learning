from typing import List


def bucket_sort(arr: List[int]):
    """桶排序"""
    min_num = min(arr)
    max_num = max(arr)
    # 桶的大小
    bucket_range = (max_num - min_num) / len(arr)
    # 桶数组
    count_list = [[] for i in range(len(arr) + 1)]
    # 向桶数组填数
    for i in arr:
        count_list[int((i - min_num) // bucket_range)].append(i)
    arr.clear()
    # 回填，这里桶内部排序直接调用了sorted
    for i in count_list:
        for j in sorted(i):
            arr.append(j)

    return arr


if __name__ == "__main__":
    nums = input("请输入一串数字, 数字之间空一个间隔：")
    arr = list(map(int, nums.rstrip().split()))
    result = bucket_sort(arr)
    print("归并排序的结果为：", result)
