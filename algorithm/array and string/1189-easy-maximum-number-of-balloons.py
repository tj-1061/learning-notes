from math import floor
from typing import List


class Solution1:
    def maximumNumberOfBalloons(self, text: str) -> int:
        cnt = 1000000
        alphabet = {
            'b':0,
            'a':0,
            'l':0,
            'o':0,
            'n':0
        }
        for c in text:
            if c in alphabet.keys():
                if c == 'l' or c == 'o':
                    alphabet[c] += 0.5
                else:
                    alphabet[c] += 1
        for _, val in alphabet.items():
            if floor(val) < cnt:
                cnt = floor(val)

        return cnt


class Solution2:
    def maximumNumberOfBalloons(self, text: str) -> int:
        from collections import Counter
        count = Counter(text)
        return min(count['b'], count['a'], count['l'] // 2, count['o'] // 2, count['n'])


if __name__ == "__main__":
    s = Solution1()
    assert s.maximumNumberOfBalloons("nlaebolko") == 1
    assert s.maximumNumberOfBalloons("loonbalxballpoon") == 2
    assert s.maximumNumberOfBalloons("leetcode") == 0

    s = Solution2()
    assert s.maximumNumberOfBalloons("nlaebolko") == 1
    assert s.maximumNumberOfBalloons("loonbalxballpoon") == 2
    assert s.maximumNumberOfBalloons("leetcode") == 0
    print("All tests passed!")
