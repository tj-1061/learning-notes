from typing import List


class Solution:
    def pascalTriangle(self, numRows: int) -> List[List[int]]:
        ans = []
        for row in range(numRows):
            row_ans = []
            for i in range(0, row + 1):
                if i == 0 or i == row:
                    row_ans.append(1)
                else:
                    row_ans.append(ans[row - 1][i - 1] + ans[row - 1][i])
            ans.append(row_ans)
        
        return ans


if __name__ == "__main__":
    s = Solution()
    assert s.pascalTriangle(5) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    assert s.pascalTriangle(1) == [[1]]
    assert s.pascalTriangle(2) == [[1], [1, 1]]
    print("All tests passed.")
