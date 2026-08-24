from typing import List


class Solution1:
    def getRow(self, rowIndex: int) -> List[int]:
        ans = [1]
        for i in range(rowIndex + 1):
            row = list()
            for j in range(0, i + 1):
                if j == 0 or j == i:
                    row.append(1)
                else:
                    row.append(ans[j] + ans[j - 1])
            ans = row
        
        return ans


class Solution2:
    def getRow(self, rowIndex: int) -> List[int]:
        ans = [1]
        for i in range(rowIndex):
            ans.append(0)
            for j in range(i + 1, 0, -1):
                ans[j] += ans[j - 1]
        
        return ans


if __name__ == "__main__":
    s = Solution1()
    assert s.getRow(3) == [1, 3, 3, 1]
    s = Solution2()
    assert s.getRow(3) == [1, 3, 3, 1]
    print("All tests passed!")
