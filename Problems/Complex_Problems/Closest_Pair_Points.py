from Problems.ClassicalProblems import distance_between_two_points
from Representations.Point import Point
from Utils.Utils import cmp_to_key
import math
import copy

class Points:
    def __init__(self):
        self.minDistance = math.inf
        self.point_1 = None
        self.point_2 = None

    def change(self, p1, p2):
        if distance_between_two_points(p1, p2) < self.minDistance:
            self.point_1 = p1
            self.point_2 = p2
            self.minDistance = distance_between_two_points(p1, p2)


class ClosestPair:
    def __init__(self, l: list):
        self.points = Points()
        self.p = l

    @staticmethod
    def compare_x(p1: Point, p2: Point):
        return p1.get_x() - p2.get_x()

    @staticmethod
    def compare_y(p1: Point, p2: Point):
        return p1.get_y() - p2.get_y()

    @staticmethod
    def brute_force(p: list, n: int, points: Points):
        min_value = math.inf

        for i in range(n):
            for j in range(i+1, n):
                if distance_between_two_points(p[i], p[j]) < min_value:
                    min_value = distance_between_two_points(p[i], p[j])
                    points.change(p[i], p[j])

        return min_value

    @staticmethod
    def strip_closest(strip: list, size: int, d: float, points: Points):
        min_value = d

        for i in range(size):
            j = i+1
            while j < size and (strip[j].get_y() - strip[i].get_y()) < min_value:
                if distance_between_two_points(strip[i], strip[j]):
                    min_value = distance_between_two_points(strip[i], strip[j])
                    points.change(strip[i], strip[j])
                j += 1

        return min_value

    @staticmethod
    def closest_util(px: list, py: list, n: int, points: Points):
        if n <= 3:
            return ClosestPair.brute_force(px, n, points)

        mid = int(n/2)
        mid_point = px[mid]

        pyl = []
        pyr = []
        li = 0
        ri = 0
        for i in range(n):
            if py[i].get_x() <= mid_point.get_x():
                pyl.append(py[i])
                li += 1
            else:
                pyr.append(py[i])
                ri += 1

        dl = ClosestPair.closest_util(px, pyl, li, points)
        dr = ClosestPair.closest_util(px[mid:], pyr, ri, points)

        d = min(dl, dr)

        strip = []
        for i in range(n):
            if math.fabs(py[i].get_x() - mid_point.get_x()) < d:
                strip.append(py[i])

        return min(d, ClosestPair.strip_closest(strip, len(strip), d, points))

    def get_closest_points(self):
        points = self.points

        px = copy.deepcopy(self.p)
        py = copy.deepcopy(self.p)

        px.sort(key=cmp_to_key(ClosestPair.compare_x))
        py.sort(key=cmp_to_key(ClosestPair.compare_y))

        ClosestPair.closest_util(px, py, len(px), points)

        return points.minDistance, points.point_1, points.point_2


if __name__ == '__main__':
    a = []
    a.append(Point(2, 3))
    a.append(Point(12, 30))
    a.append(Point(40, 50))
    a.append(Point(5, 1))
    a.append(Point(12, 10))
    a.append(Point(3, 4))

    asd = ClosestPair(a)

    print(asd.get_closest_points())
