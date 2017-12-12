from Representations.Point import Point
from Representations.Line import Line
from Representations.Circle import Circle
from Representations.Polygon import Polygon
from Representations.LineSegment import LineSegment
import math
import copy


def distance_between_two_points(pa: Point, pb: Point):
    """
    Get a distance between two points
    :param pa - Point A
    :param pb - Point B
    :return distance between point A and B
    """
    return math.sqrt(pow(pb.get_x() - pa.get_x(), 2) + pow(pb.get_y() - pa.get_y(), 2))


def distance_between_one_line_and_one_point(p: Point, l: Line):
    """
    Get a distance between one line and one point
    :param p: one point
    :param l: one line
    :return: distance between p and l
    """
    return (math.fabs(l.get_a() * p.get_x() + l.get_a() * p.get_y() + l.get_c())) / \
           math.sqrt(pow(l.get_a(), 2) + pow(l.get_b(), 2))


def area_of_a_circle(c: Circle):
    """
    Area for circle
    :param c: a circle
    :return: area
    """
    return math.pi * pow(c.get_radius(), 2)


def polygon_sort(poly: Polygon):
    corners = poly.get_list_points()
    n = len(corners)
    cx = 0
    cy = 0

    for i in corners:
        cx += i.get_x()
        cy += i.get_y()

    cx = cx / float(n)
    cy = cy / float(n)

    corners_with_angles = []
    for i in corners:
        dx = i.get_x() - cx
        dy = i.get_y() - cy
        an = (math.atan2(dy, dx) + 2.0 * math.pi) % (2.0 * math.pi)
        corners_with_angles.append((dx, dy, an))

    corners_with_angles.sort(key=lambda tup: tup[2])
    return corners_with_angles


def polygon_area(poly: Polygon):
    """
    Polygon area using Shoelace formula.
    Algorithm based http://www.geeksforgeeks.org/area-of-a-polygon-with-given-n-ordered-vertices/
    :param poly: one polygon
    :return: area for polygon
    """
    corners = polygon_sort(poly)
    n = len(corners)
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0

    return area


def convex_polygon(poly: Polygon):
    if len(poly.get_list_points()) < 3:
        return False

    list_points = poly.get_list_points()

    res = 0
    for i in range(len(list_points)):
        p = list_points[i]
        tmp = list_points[((i+1) % len(list_points))]
        vx = tmp.get_x() - p.get_x()
        vy = tmp.get_y() - p.get_y()
        v = Point(vx, vy)
        u = list_points[((i+2) % len(list_points))]

        if i == 0:
            res = u.get_x() * v.get_y() - u.get_y() * v.get_x() + v.get_x() * p.get_y() - v.get_y() * p.get_x()
        else:
            new_res = u.get_x() * v.get_y() - u.get_y() * v.get_x() + v.get_x() * p.get_y() - v.get_y() * p.get_x()
            if (new_res > 0 and res < 0) or (new_res < 0 and res > 0):
                return False

    return True

def side_of_circle(c: Circle, p: Point):
    distance = distance_between_two_points(c.get_centre(), p)
    if distance < c.get_radius():
        return 1
    elif distance == c.get_radius():
        return 0
    else:
        return -1


def __nearest_distance(seg: LineSegment, p: Point):
    a = p.get_x() - seg.get_a().get_x()
    b = p.get_y() - seg.get_a().get_y()
    c = seg.get_b().get_x() - seg.get_a().get_x()
    d = seg.get_b().get_x() - seg.get_a().get_y()

    dot = a * c + b * d
    q = c ** 2 + d ** 2
    param = -1

    if q != 0:
        param = dot / q

    if param < 0:
        xx = seg.get_a().get_x()
        yy = seg.get_a().get_y()
    elif param > 1:
        xx = seg.get_b().get_x()
        yy = seg.get_b().get_y()
    else:
        xx = seg.get_a().get_x() + param * c
        yy = seg.get_a().get_y() + param * d

    dx = p.get_x() - xx
    dy = p.get_y() - yy
    return math.sqrt(dx ** 2 + dy ** 2)


def closest_point(seg: LineSegment, points: list):
    """
    Algorithm for get closest point between a line segment
    Algorithm based in https://goo.gl/PkLqhe
    :param seg: one line segment
    :param points: a list of points
    :return: a point more closest
    """
    distance = math.inf
    point = None

    for i in points:
        value = __nearest_distance(seg, i)
        if value < distance:
            distance = value
            point = Point(i.get_x(), i.get_y())

    return point


def orient_2d(a: Point, b: Point, c: Point):
    """
    Orientation of tree points
    Algorithm based in http://www.geeksforgeeks.org/orientation-3-ordered-points/
    :param a: point 1
    :param b: point 2
    :param c: point 3
    :return: orientation
    """
    first = (b.get_y() - a.get_y()) * (c.get_x() - b.get_x())
    second = (c.get_y() - b.get_y()) * (b.get_x() - a.get_x())
    det = first - second

    if det == 0:
        return 0
    elif det > 0:
        return 1
    else:
        return -1


def __point_in_segment(p: Point, s: LineSegment):
    px = p.get_x()
    py = p.get_y()

    sa_x = s.get_a().get_x()
    sa_y = s.get_a().get_y()
    sb_x = s.get_b().get_x()
    sb_y = s.get_b().get_y()

    if px <= max(sa_x, sb_x) and px >= min(sa_x, sb_x) and \
                    py <= max(sa_y, sb_y) and py >= min(sa_y, sb_y):
        return True
    else:
        return False


def __points_orientation(p: Point, q: Point, r: Point):
    value = (q.get_y() - p.get_y()) * (r.get_x() - q.get_x()) - (q.get_x() - p.get_x()) * (r.get_y() - q.get_y())

    if value == 0:
        return 0
    elif value > 0:
        return 1
    else:
        return 2


def intersection_two_lines_segments(seg1: LineSegment, seg2: LineSegment):
    """
    Check that two line segments meet
    Algorithm based in http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    :param seg1: segment one
    :param seg2: segment two
    :return: if exist intersection or not
    """
    o1 = __points_orientation(seg1.get_a(), seg1.get_b(), seg2.get_a())
    o2 = __points_orientation(seg1.get_a(), seg1.get_b(), seg2.get_b())
    o3 = __points_orientation(seg2.get_a(), seg2.get_b(), seg1.get_a())
    o4 = __points_orientation(seg2.get_a(), seg2.get_b(), seg1.get_b())

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and __point_in_segment(seg2.get_a(), seg1):
        return True
    if o2 == 0 and __point_in_segment(seg2.get_b(), seg1):
        return True
    if o3 == 0 and __point_in_segment(seg1.get_a(), seg2):
        return True
    if o4 == 0 and __point_in_segment(seg1.get_b(), seg2):
        return True

    return False


def point_in_polygon(p: Point, polygon: Polygon):
    cn = 0
    v = copy.deepcopy(polygon.get_list_points())
    v.append(v[0])

    for i in range(len(v)-1):
        if (v[i].get_y() <= p.get_y() and v[i+1].get_y() > p.get_y()) or \
           (v[i].get_y() > p.get_y() and v[i+1].get_y() <= p.get_y()):

            vt = (p.get_y() - v[i].get_y()) / float(v[i+1].get_y() - v[i].get_y())
            if p.get_x() < (v[i].get_x() + vt * (v[i+1].get_x() - v[i].get_x())):
                cn += 1

    return True if (cn % 2) == 1 else False


class EarClipping:
    def __init__(self, polygon: Polygon):
        self.points = polygon.get_list_points()

    @staticmethod
    def __dot(a, b):
        return a[0] * b[0] + a[1] * b[1]

    @staticmethod
    def __cap(a):
        return -a[1], a[0]

    @staticmethod
    def __diff(a, b):
        return (a[0] - b[0]), (a[1] - b[1])

    @staticmethod
    def __add(a, b):
        return (a[0] + b[0]), (a[1] + b[1])

    @staticmethod
    def __triangle_area(a, b, c):
        return EarClipping.__dot(EarClipping.__diff(c, a), EarClipping.__cap(EarClipping.__diff(b, a)))

    @staticmethod
    def __point_left_to_line(q, p1, p2):
        return EarClipping.__dot(EarClipping.__diff(q, p1), EarClipping.__cap(EarClipping.__diff(p2, p1))) >= 0

    @staticmethod
    def __is_clockwise(points):
        length = len(points)
        sum = (points[0][0] - points[length - 1][0]) * (points[0][1] + points[length - 1][1])
        for i in range(1, length):
            sum += (points[i][0] - points[i - 1][0]) * (points[i][1] + points[i - 1][1])
        return sum < 0

    @staticmethod
    def __is_convex(v_prev, v, v_next):
        return EarClipping.__triangle_area(v_prev, v, v_next) > 0

    @staticmethod
    def __no_vertex_in_triangle(points, v_prev, v, v_next):
        for w in points:
            if w == v or w == v_prev or w == v_next:
                continue
            if EarClipping.__point_left_to_line(w, v_prev, v) and EarClipping.__point_left_to_line(w, v, v_next) and \
                    EarClipping.__point_left_to_line(w, v_next,v_prev):
                return False
        return True

    @staticmethod
    def __is_ear(points, v_prev, v, v_next):
        return EarClipping.__is_convex(v_prev, v, v_next) and EarClipping.__no_vertex_in_triangle(points, v_prev, v, v_next)

    @staticmethod
    def ears_finding(points):
        ears = []
        if not EarClipping.__is_clockwise(points):
            points.reverse()
        length = len(points)
        for i in range(0, length):
            if EarClipping.__is_ear(points, points[(i - 1) % length], points[i], points[(i + 1) % length]):
                ears.append(points[i])
        return ears

    @staticmethod
    def ears_clipping(points, ears):
        if len(ears) == 0:
            return []

        edges = []
        length = len(points)
        e = ears[0]

        while len(points) > 3:
            ind = points.index(e)

            prev_pred = points[(ind - 2) % length]
            pred = points[(ind - 1) % length]
            succ = points[(ind + 1) % length]
            next_succ = points[(ind + 2) % length]

            edges.append(LineSegment(Point(pred[0], pred[1]), Point(succ[0], succ[1])))
            points.remove(e)
            length -= 1
            ears.remove(e)

            if EarClipping.__is_ear(points, prev_pred, pred, succ):
                if pred not in ears:
                    ears.append(pred)
            else:
                if pred in ears:
                    ears.remove(pred)
            if EarClipping.__is_ear(points, pred, succ, next_succ):
                if succ not in ears:
                    ears.append(succ)
            else:
                if succ in ears:
                    ears.remove(succ)
            if len(ears) > 0:
                e = ears[0]
            else:
                return []
        return edges
