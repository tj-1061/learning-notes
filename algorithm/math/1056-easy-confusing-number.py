from typing import List


class Solution:
    def confusing_number(self, nums: List[int]) -> int:
        rot = [0, 1, -1, -1, -1, -1, 9, -1, 8, 6]
        dum = nums
        dup = 0

        while dum:
            dum, m = divmod(dum, 10)
            if rot[m] < 0:
                return False
            dup = dup * 10 + rot[m]
        
        return nums != dup

if __name__ == "__main__":
    s = Solution()
    assert s.confusing_number(89)
    print('All tests passed!')
