from typing import List


class Solution:
    def distanceBetweenBusStops(self, distance: List[int], start: int, destination: int) -> int:
        if start > destination:
            start, destination = destination, start
        return min(
            sum(distance[0:start] + distance[destination:len(distance)]),
            sum(distance[start:destination])
        )


if __name__ == "__main__":
    solution = Solution()
    assert solution.distanceBetweenBusStops([1, 2, 3, 4], 0, 1) == 1
    assert solution.distanceBetweenBusStops([1, 2, 3, 4], 0, 2) == 3
    assert solution.distanceBetweenBusStops([1, 2, 3, 4], 0, 3) == 4
    assert solution.distanceBetweenBusStops([7,10,1,12,11,14,5,0], 7, 2) == 17
    print("All tests passed!")

