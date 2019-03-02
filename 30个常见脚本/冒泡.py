"""
冒泡排序算法（亦称稳定排序算法）的原理如下：
    1、比较相邻的元素。如果第一个比第二个大，就交换他们两个。
    2、对每一对相邻元素做同样的工作，从开始第一对到结尾的最后一对。在这一点，最后的元素应该会是最大的数。
    3、针对所有的元素重复以上的步骤，除了最后一个。
    4、持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
"""
list1 = [56, 12, 1, 8, 354, 10, 100, 34, 56, 7, 23, 456, 234, -58]
def sortport(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums
    
print(sortport(list1))