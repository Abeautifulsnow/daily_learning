"""
将待排序集合中处于同一个值域的元素存入同一个桶中，
也就是根据元素值特性将集合拆分为多个区域，
则拆分后形成的多个桶，从值域上看是处于有序状态的。
对每个桶中元素进行排序，则所有桶中元素构成的集合是已排序的。
"""

"""算法实现
1.根据待排序集合中 `最大元素` 和 `最小元素` 的差值范围和映射规则，确定申请的桶个数(基于整个集合的长度或者其他)；
2.遍历排序序列，将每个元素放到对应的桶里去(集合里面的值 除以 桶大小 就可以按顺序得到需要放在第几个桶)；
3.对不是空的桶进行排序；
4.按顺序访问桶，将桶中的元素依次放回到原序列中对应的位置，完成排序。
"""

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
