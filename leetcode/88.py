"""
No.88
题目：合并两个有序数组
难度：简单
"""

####################################
# Answer1                          #
# Time complexity：O((n+m)log(n+m))#
# Space complexity：O(1)           #
###################################
class Solution1:
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: void Do not return anything, modify nums1 in-place instead.
        """
        nums1[:] = sorted(nums1[:m] + nums2)


####################################
# Answer2                          #
# Time complexity：O(n+m)          #
# Space complexity：O(m)           #
###################################
class Solution2:
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: void Do not return anything, modify nums1 in-place instead.
        """
        nums1_copy = nums1[:m]
        nums1[:] = []

        # pointers
        p1, p2 = 0, 0

        # Compare elements from nums1_copy and nums2
        # and add the smallest one into nums1.
        while p1 < m and p2 < n:
            if nums1_copy[p1] < nums2[p2]:
                nums1.append(nums1_copy[p1])
                p1 += 1
            else:
                nums1.append(nums2[p2])
                p2 += 1
        
        # if there are still elements to add.
        if p1 < m:
            nums1[(p1 + p2):] = nums1_copy[p1:]
        if p2 < n:
            nums1[(p1 + p2):] = nums2[p2:]


####################################
# Answer3                          #
# Time complexity：O(n+m)          #
# Space complexity：O(1)           #
###################################
class Solution3:
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: void Do not return anything, modify nums1 in-place instead.
        """
        # pointers
        p1, p2 = m - 1, n - 1

        # set pointers to nums1
        p = m + n - 1
        
        # while there are still elements to compare
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] < nums2[p2]:
                nums1[p] = nums2[p2]
                p2 -= 1
            else:
                nums1[p] = nums1[p1]
                p1 -= 1
            p -= 1
        
        # add missing elements from nums2
        nums1[:p2 + 1] = nums2[:p2 + 1]
