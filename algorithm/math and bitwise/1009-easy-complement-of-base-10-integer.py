from typing import List


class Solution:
    def bitwiseComplement(self, n: int) -> int:
        num_bits = n.bit_length() or 1
        mask = (1 << num_bits) - 1
        return n ^ mask


if __name__ == "__main__":
    s = Solution()
    assert s.bitwiseComplement(5) == 2
    assert s.bitwiseComplement(7) == 0
    assert s.bitwiseComplement(10) == 5
    print("All tests passed!")
