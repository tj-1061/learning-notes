from typing import List


class Solution:
    def minCostToMoveChips(self, position: List[int]) -> int:
        from collections import Counter
        cnt = Counter(pos % 2 for pos in position)
        return min(cnt[0], cnt[1])


if __name__ == "__main__":
    s = Solution()
    assert s.minCostToMoveChips([1, 2, 3]) == 1
    assert s.minCostToMoveChips([2, 2, 2, 3, 3]) == 2
    assert s.minCostToMoveChips([1, 1000000000]) == 1
    print("All tests passed.")
