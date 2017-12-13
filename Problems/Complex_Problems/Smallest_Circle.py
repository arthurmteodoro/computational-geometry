import math
import copy
import random
from Representations.Point import Point
from Representations.Circle import Circle
import Problems.ClassicalProblems as classics


# Algorithm based in https://www.nayuki.io/page/smallest-enclosing-circle

def make_circle(points: list):
    shuffled = copy.deepcopy(points)
    random.shuffle(shuffled)

    # Adicionar progressivamente os pontos no circulo ou recalculá-lo
    c = None
    for (i, p) in enumerate(shuffled):
        # side of circle: 1 = dentro, 0 = no raio, -1 fora
        if c is None or classics.side_of_circle(c, p) == -1:
            c = _make_circle_one_point(shuffled[: i + 1], p)
    return c


# Um ponto de fronteira conhecidos
def _make_circle_one_point(points: list, p: Point):
    c = Circle(p, 0)
    for (i, q) in enumerate(points):
        # side of circle: 1 = dentro, 0 = no raio, -1 fora
        if classics.side_of_circle(c, q) == -1:
            if c.get_radius() == 0.0:
                c = make_diameter(p, q)
            else:
                c = _make_circle_two_points(points[: i + 1], p, q)
    return c


# Dois pontos de fronteira conhecido
def _make_circle_two_points(points: list, p: Point, q: Point):
    circ = make_diameter(p, q)
    left = None
    right = None
    px = p.get_x()
    py = p.get_y()
    qx = q.get_x()
    qy = q.get_y()

    # para cada ponto que nao está no circulo
    for r in points:
        if classics.side_of_circle(circ, r) >= 0:
            continue

        # Formar uma circunferência e classificá-la no lado esquerdo ou direito
        cross = _cross_product(px, py, qx, qy, r.get_x(), r.get_y())
        c = make_circumcircle(p, q, r)
        if c is None:
            continue
        elif cross > 0.0 and (
                left is None or _cross_product(px, py, qx, qy, c.get_centre().get_x(), c.get_centre().get_y()) >
                _cross_product(px, py, qx, qy, left.get_centre().get_x(), left.get_centre().get_y())):
            left = c
        elif cross < 0.0 and (
                right is None or _cross_product(px, py, qx, qy, c.get_centre().get_x(), c.get_centre().get_y()) <
                _cross_product(px, py, qx, qy, right.get_centre().get_x(), right.get_centre().get_y())):
            right = c

    # selecionar qual circulo vai retornar
    if left is None and right is None:
        return circ
    elif left is None:
        return right
    elif right is None:
        return left
    else:
        return left if (left.get_radius() <= right.get_radius()) else right


def make_circumcircle(p0: Point, p1: Point, p2: Point):
    ax = p0.get_x()
    ay = p0.get_y()
    bx = p1.get_x()
    by = p1.get_y()
    cx = p2.get_x()
    cy = p2.get_y()
    ox = (min(ax, bx, cx) + max(ax, bx, cx)) / 2.0
    oy = (min(ay, by, cy) + max(ay, by, cy)) / 2.0
    ax -= ox
    ay -= oy
    bx -= ox
    by -= oy
    cx -= ox
    cy -= oy
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None
    x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    ra = math.hypot(x - p0.get_x(), y - p0.get_y())
    rb = math.hypot(x - p1.get_x(), y - p1.get_y())
    rc = math.hypot(x - p2.get_x(), y - p2.get_y())
    return Circle(Point(x, y), max(ra, rb, rc))


def make_diameter(p0: Point, p1: Point):
    cx = (p0.get_x() + p1.get_x()) / 2.0
    cy = (p0.get_y() + p1.get_y()) / 2.0
    r0 = math.hypot(cx - p0.get_x(), cy - p0.get_y())
    r1 = math.hypot(cx - p1.get_x(), cy - p1.get_y())
    return Circle(Point(cx, cy), max(r0, r1))


# Retorna duas vezes a área assinada do triângulo definido por (x0, y0), (x1, y1), (x2, y2).
def _cross_product(x0, y0, x1, y1, x2, y2):
    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)


if __name__ == '__main__':
    points = [Point(1, 1), Point(4, 3), Point(5, 3), Point(3, 1)]
    c = make_circle(points)
