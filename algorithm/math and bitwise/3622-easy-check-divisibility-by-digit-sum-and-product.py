from typing import List


class Solution:
    def check_divisibility(self, n: int) -> bool:
        n1, s, p = n, 0, 1
        while n1:
            n1, v = divmod(n1, 10)
            s += v
            p *= v
        return n % (s + p) == 0


if __name__ == "__main__":
    s = Solution()
    assert s.check_divisibility(99) == True
    assert s.check_divisibility(101) == False
    print("All tests passed!")
