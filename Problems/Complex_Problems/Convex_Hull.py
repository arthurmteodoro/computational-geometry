from Representations.Point import Point
from Problems.ClassicalProblems import orient_2d
from Utils.Utils import cmp_to_key


class MidPoint:
    def __init__(self):
        self.mid = Point(0, 0)


class ConvexHull:
    def __init__(self, points):
        self.pts = points

    @staticmethod
    def quad(p: Point):
        if p.get_x() >= 0 and p.get_y() >= 0:
            return 1
        if p.get_x() <= 0 and p.get_y() >= 0:
            return 2
        if p.get_x() <= 0 and p.get_y() <= 0:
            return 3
        return 4

    """@staticmethod
    def compare(p1: Point, q1: Point):
        px = p1.get_x() - mid_point.mid.get_x()
        py = p1.get_y() - mid_point.mid.get_y()
    
        qx = q1.get_x() - mid_point.mid.get_x()
        qy = q1.get_y() - mid_point.mid.get_y()
    
        p = Point(px, py)
        q = Point(qx, qy)
    
        one = ConvexHull.quad(p)
        two = ConvexHull.quad(q)
    
        if one != two:
            if one < two:
                return 1
            else:
                return -1
        return 1 if (p.get_y() * q.get_x()) < (q.get_y() * p.get_x()) else -1"""

    @staticmethod
    def merger(a: list, b: list):
        n1 = len(a)
        n2 = len(b)

        ia = 0
        ib = 0
        for i in range(1, n1):
            if a[i].get_x() > a[ia].get_x():
                ia = i

        for i in range(1, n2):
            if b[i].get_x() < b[ib].get_x():
                ib = i

        ind_a = ia
        ind_b = ib
        done = False
        while not done:
            done = True
            while orient_2d(b[ind_b], a[ind_a], a[(ind_a + 1) % n1]) >= 0:
                ind_a = (ind_a + 1) % n1

            while orient_2d(a[ind_a], b[ind_b], b[(n2 + ind_b - 1) % n2]) <= 0:
                ind_b = (n2 + ind_b - 1) % n2
                done = False

        upper_a = ind_a
        upper_b = ind_b

        ind_a = ia
        ind_b = ia
        done = False
        g = 0
        while not done:
            done = True
            while orient_2d(a[ind_a], b[ind_b], b[(ind_b + 1) % n2]) >= 0:
                ind_b = (ind_b + 1) % n2

            while orient_2d(b[ind_b], a[ind_a], a[(n1 + ind_a - 1) % n1]) <= 0:
                ind_a = (n1 + ind_a - 1) % n1
                done = False

        lower_a = ind_a
        lower_b = ind_b
        ret = []

        ind = upper_a
        ret.append(a[upper_a])

        while ind != lower_a:
            ind = (ind + 1) % n1
            ret.append(a[ind])

        ind = lower_b
        ret.append(b[lower_b])
        while ind != upper_b:
            ind = (ind + 1) % n2
            ret.append(b[ind])

        return ret

    @staticmethod
    def brute_hull(a: list):
        if len(a) < 3:
            return

        hull = []
        l = 0
        for i in range(1, len(a)):
            if a[i].get_x() < a[l].get_x():
                l = i

        p = l

        # while true for emulation do while
        while True:
            hull.append(a[p])
            q = (p + 1) % len(a)

            for i in range(len(a)):
                if orient_2d(a[p], a[i], a[q]) == -1:
                    q = i

            p = q

            if not p != l:
                break

        return hull

    @staticmethod
    def divide(a: list):
        if len(a) <= 5:
            return ConvexHull.brute_hull(a)

        left = []
        right = []
        for i in range(int(len(a) / 2)):
            left.append(a[i])
        for i in range(int(len(a) / 2), len(a)):
            right.append(a[i])

        left_hull = ConvexHull.divide(left)
        right_hull = ConvexHull.divide(right)

        return ConvexHull.merger(left_hull, right_hull)

    @staticmethod
    def comp(x, y):
        if x.get_x() > y.get_x():
            return 1
        elif x.get_x() == y.get_x():
            return 0
        else:
            return -1

    def calcule(self):
        self.pts.sort(key=cmp_to_key(ConvexHull.comp))
        hull = ConvexHull.divide(self.pts)
        return hull


if __name__ == '__main__':
    a = []
    a.append(Point(0, 0))
    a.append(Point(1, -4))
    a.append(Point(-1, -5))
    a.append(Point(-5, -3))
    a.append(Point(-3, -1))
    a.append(Point(-1, -3))
    a.append(Point(-2, -2))
    a.append(Point(-1, -1))
    a.append(Point(-2, -1))
    a.append(Point(-1, 1))

    convex = ConvexHull(a)
    hull = convex.calcule()

    for i in hull:
        print(str(i.get_x()) + ' ' + str(i.get_y()))
