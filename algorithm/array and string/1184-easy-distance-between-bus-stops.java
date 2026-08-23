class Solution {
    public int distanceBetweenBusStops(int[] distance, int start, int destination) {
        if (start > destination) {
            int temp = start;
            start = destination;
            destination = temp;
        }
        int clockwiseDistance = 0;
        for (int i = start; i < destination; i++) {
            clockwiseDistance += distance[i];
        }
        int totalDistance = 0;
        for (int d : distance) {
            totalDistance += d;
        }
        return Math.min(clockwiseDistance, totalDistance - clockwiseDistance);
    }
}