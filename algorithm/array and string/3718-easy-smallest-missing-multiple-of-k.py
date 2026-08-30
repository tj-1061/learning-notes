from typing import List


class Solution:
    def missingMultiple(self, nums: List[int], k: int) -> int:
        multiple = k
        nums_set = set(nums)
        
        while True:
            if multiple not in nums_set:
                return multiple
            multiple += k


if __name__ == "__main__":
    s = Solution()
    assert s.missingMultiple([1, 2, 3, 4, 5], 2) == 6
    assert s.missingMultiple([2, 4, 6, 8], 2) == 10
    assert s.missingMultiple([3, 6, 9], 3) == 12
    assert s.missingMultiple([1, 3, 5], 2) == 2
    assert s.missingMultiple([1, 2, 3, 4, 5], 1) == 6
    print("All tests passed.")
