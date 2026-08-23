from typing import List


class Solution:
    def single_row_keyboard(self, keyboard: str, word: str) -> int:
        pos = {ch: i for i, ch in enumerate(keyboard)}
        total_time = 0
        current_pos = 0

        for ch in word:
            total_time += abs(pos[ch] - current_pos)
            current_pos = pos[ch]

        return total_time

if __name__ == "__main__":
    s = Solution()
    assert s.single_row_keyboard(
        keyboard="abcdefghijklmnopqrstuvwxyz",
        word="cba"
    ) == 4
    print("All tests passed!")
