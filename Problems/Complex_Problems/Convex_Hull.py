from Representations.Point import Point
from Problems.ClassicalProblems import orient_2d, distance_between_two_points
from Utils.Utils import cmp_to_key
import math


class P0:
    def __init__(self):
        self.p0 = Point(0, 0)


class ConvexHull:
    def __init__(self, points):
        self.pts = points
        self.p0 = P0()

    def next_to_top(self, pilha: list):
        p = pilha.pop()
        res = pilha[-1]
        pilha.append(p)
        return res

    @staticmethod
    def swap(p1: Point, p2: Point):
        temp = p1
        p1 = p2
        p2 = temp

    def distSq(self, p1: Point, p2: Point):
        return math.pow(distance_between_two_points(p1, p2), 2)

    def compare(self, p1: Point, p2: Point):
        o = orient_2d(self.p0.p0, p1, p2)
        if o == 0:
            if self.distSq(self.p0.p0, p2) >= self.distSq(self.p0.p0, p1):
                return -1
            else:
                return 1
        return o

    def convex_hull(self):
        y_min = self.pts[0].get_y()
        min = 0

        for i in range(len(self.pts)):
            y = self.pts[i].get_y()

            if (y < y_min) or ((y_min == y) and (self.pts[i].get_x() < self.pts[min].get_x())):
                y_min = self.pts[i].get_y()
                min = i

        ConvexHull.swap(self.pts[0], self.pts[min])

        self.p0.p0 = self.pts[0]
        sort = sorted(self.pts[1:], key=cmp_to_key(self.compare))
        self.pts.clear()
        self.pts.append(self.p0.p0)
        for i in sort:
            self.pts.append(i)

        m = 1
        for i in range(1, len(self.pts)):
            while (i < len(self.pts)-1) and orient_2d(self.p0.p0, self.pts[i], self.pts[i+1]) == 0:
                i += 1

            self.pts[m] = self.pts[i]
            m += 1

        if m < 3:
            return

        S = []
        S.append(self.pts[0])
        S.append(self.pts[1])
        S.append(self.pts[2])

        for i in range(3, m):
            while orient_2d(self.next_to_top(S), S[-1], self.pts[i]) != -1:
                S.pop()
            S.append(self.pts[i])

        return S


if __name__ == '__main__':
    a = []
    a.append(Point(0, 3))
    a.append(Point(1, 1))
    a.append(Point(2, 2))
    a.append(Point(4, 4))
    a.append(Point(0, 0))
    a.append(Point(1, 2))
    a.append(Point(3, 1))
    a.append(Point(3, 3))

    convex = ConvexHull(a)
    convex.convex_hull()
