from typing import List


class Solution:
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        if m * n != len(original):
            return []
        ans = list()
        i = n
        while i <= len(original):
            ans.append(original[i - n: i])
            i += n
        return ans


if __name__ == "__main__":
    s = Solution()
    assert s.construct2DArray([1, 2, 3, 4], 2, 2) == [[1, 2], [3, 4]]
    assert s.construct2DArray([1, 2, 3], 1, 3) == [[1, 2, 3]]
    assert s.construct2DArray([1, 2], 1, 1) == []
    assert s.construct2DArray([3], 1, 2) == []
    assert s.construct2DArray([1, 2, 3, 4], 2, 4) == []
    print("All tests passed.")
