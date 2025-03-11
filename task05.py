"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List


def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    largest = 0
    total = 0

    for i, num in enumerate(nums):
        total += num
        if i >= k:  # смещаем вправо
            total -= nums[i - k]
        if i >= k - 1:  # находим наибольшее на данный момент ПОСЛЕ СМЕЩЕНИЯ
            largest = max(largest, total)
    return largest


nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(find_maximal_subarray_sum(nums, k))  # 16
