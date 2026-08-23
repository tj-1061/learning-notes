from collections import Counter
from typing import List


class Solution1:
    def largest_unique_number(self, nums: List[int]) -> int:
        c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for d in nums:
            c[d] += 1
        for i in [9,8,7,6,5,4,3,2,1,0]:
            if c[i] == 1:
                return i
        return -1

class Solution2:
    def largest_unique_number(self, nums: List[int]) -> int:
        c = Counter(nums)
        return max((k for k, v in c.items() if v == 1), default=-1)


if __name__ == "__main__":
    s = Solution1()
    assert s.largest_unique_number([5, 7, 3, 9, 4]) == 9
    assert s.largest_unique_number([9, 9, 8, 8]) == -1
    print("All tests passed for Solution1!")

    s = Solution2()
    assert s.largest_unique_number([5, 7, 3, 9, 4]) == 9
    assert s.largest_unique_number([9, 9, 8, 8]) == -1
    print("All tests passed for Solution2!")
