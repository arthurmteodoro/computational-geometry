import heapq
import itertools
import math
from Representations.LineSegment import LineSegment
from Representations.Point import Point as P

# auxiliary classes


class Point:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Event:
    x = 0.0
    p = None
    a = None
    valid = True

    def __init__(self, x, p, a):
        self.x = x
        self.p = p
        self.a = a
        self.valid = True


class Arc:
    p = None
    p_prev = None
    p_next = None
    e = None
    s0 = None
    s1 = None

    def __init__(self, p, a=None, b=None):
        self.p = p
        self.p_prev = a
        self.p_next = b
        self.e = None
        self.s0 = None
        self.s1 = None


class Segment:
    start = None
    end = None
    done = False

    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False

    def finish(self, p):
        if self.done:
            return
        self.end = p
        self.done = True


class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def push(self, item):
        # check for duplicate
        if item in self.entry_finder:
            return
        count = next(self.counter)
        # use x-coordinate as a primary key (heapq in python is min-heap)
        entry = [item.x, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove_entry(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = 'Removed'

    def pop(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def top(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.entry_finder[item]
                self.push(item)
                return item
        raise KeyError('top from an empty priority queue')

    def empty(self):
        return not self.pq


# voronoi class


class Voronoi:
    def __init__(self, points):
        self.output = []  # list of line segment
        self.arc = None  # binary tree for parabola arcs

        self.points = PriorityQueue()  # site events
        self.event = PriorityQueue()  # circle events

        # bounding box
        self.x0 = -50.0
        self.x1 = -50.0
        self.y0 = 550.0
        self.y1 = 550.0

        # insert points to site event
        for pts in points:
            point = Point(pts.get_x(), pts.get_y())
            self.points.push(point)
            # keep track of bounding box size
            if point.x < self.x0:
                self.x0 = point.x
            if point.y < self.y0:
                self.y0 = point.y
            if point.x > self.x1:
                self.x1 = point.x
            if point.y > self.y1:
                self.y1 = point.y

        # add margins to the bounding box
        dx = (self.x1 - self.x0 + 1) / 5.0
        dy = (self.y1 - self.y0 + 1) / 5.0
        self.x0 = self.x0 - dx
        self.x1 = self.x1 + dx
        self.y0 = self.y0 - dy
        self.y1 = self.y1 + dy

    def process(self):
        while not self.points.empty():
            if not self.event.empty() and (self.event.top().x <= self.points.top().x):
                self.process_event()  # handle circle event
            else:
                self.process_point()  # handle site event

        # after all points, process remaining circle events
        while not self.event.empty():
            self.process_event()

        self.finish_edges()

    def process_point(self):
        # get next event from site pq
        p = self.points.pop()
        # add new arc (parabola)
        self.arc_insert(p)

    def process_event(self):
        # get next event from circle pq
        e = self.event.pop()

        if e.valid:
            # start new edge
            s = Segment(e.p)
            self.output.append(s)

            # remove associated arc (parabola)
            a = e.a
            if a.p_prev is not None:
                a.p_prev.p_next = a.p_next
                a.p_prev.s1 = s
            if a.p_next is not None:
                a.p_next.p_prev = a.p_prev
                a.p_next.s0 = s

            # finish the edges before and after a
            if a.s0 is not None:
                a.s0.finish(e.p)
            if a.s1 is not None:
                a.s1.finish(e.p)

            # recheck circle events on either side of p
            if a.p_prev is not None:
                self.check_circle_event(a.p_prev, e.x)
            if a.p_next is not None:
                self.check_circle_event(a.p_next, e.x)

    def arc_insert(self, p):
        if self.arc is None:
            self.arc = Arc(p)
        else:
            # find the current arcs at p.y
            i = self.arc
            while i is not None:
                flag, z = self.intersect(p, i)
                if flag:
                    # new parabola intersects arc i
                    flag, zz = self.intersect(p, i.p_next)
                    if (i.p_next is not None) and (not flag):
                        i.p_next.p_prev = Arc(i.p, i, i.p_next)
                        i.p_next = i.p_next.p_prev
                    else:
                        i.p_next = Arc(i.p, i)
                    i.p_next.s1 = i.s1

                    # add p between i and i.p_next
                    i.p_next.p_prev = Arc(p, i, i.p_next)
                    i.p_next = i.p_next.p_prev

                    i = i.p_next  # now i points to the new arc

                    # add new half-edges connected to i's endpoints
                    seg = Segment(z)
                    self.output.append(seg)
                    i.p_prev.s1 = i.s0 = seg

                    seg = Segment(z)
                    self.output.append(seg)
                    i.p_next.s0 = i.s1 = seg

                    # check for new circle events around the new arc
                    self.check_circle_event(i, p.x)
                    self.check_circle_event(i.p_prev, p.x)
                    self.check_circle_event(i.p_next, p.x)

                    return

                i = i.p_next

            # if p never intersects an arc, append it to the list
            i = self.arc
            while i.p_next is not None:
                i = i.p_next
            i.p_next = Arc(p, i)

            # insert new segment between p and i
            x = self.x0
            y = (i.p_next.p.y + i.p.y) / 2.0
            start = Point(x, y)

            seg = Segment(start)
            i.s1 = i.p_next.s0 = seg
            self.output.append(seg)

    def check_circle_event(self, i, x0):
        # look for a new circle event for arc i
        if (i.e is not None) and (i.e.x != self.x0):
            i.e.valid = False
        i.e = None

        if (i.p_prev is None) or (i.p_next is None): return

        flag, x, o = self.circle(i.p_prev.p, i.p, i.p_next.p)
        if flag and (x > self.x0):
            i.e = Event(x, o, i)
            self.event.push(i.e)

    def circle(self, a, b, c):
        # check if bc is a "right turn" from ab
        if ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) > 0: return False, None, None

        # Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

        if G == 0: return False, None, None  # Points are co-linear

        # point o is the center of the circle
        ox = 1.0 * (D * E - B * F) / G
        oy = 1.0 * (A * F - C * E) / G

        # o.x plus radius equals max x coord
        x = ox + math.sqrt((a.x - ox) ** 2 + (a.y - oy) ** 2)
        o = Point(ox, oy)

        return True, x, o

    def intersect(self, p, i):
        # check whether a new parabola at point p intersect with arc i
        if i is None:
            return False, None
        if i.p.x == p.x: return False, None

        a = 0.0
        b = 0.0

        if i.p_prev is not None:
            a = (self.intersection(i.p_prev.p, i.p, 1.0 * p.x)).y
        if i.p_next is not None:
            b = (self.intersection(i.p, i.p_next.p, 1.0 * p.x)).y

        if ((i.p_prev is None) or (a <= p.y)) and ((i.p_next is None) or (p.y <= b)):
            py = p.y
            px = 1.0 * (i.p.x ** 2 + (i.p.y - py) ** 2 - p.x ** 2) / (2 * i.p.x - 2 * p.x)
            res = Point(px, py)
            return True, res
        return False, None

    def intersection(self, p0, p1, l):
        # get the intersection of two parabolas
        p = p0
        if p0.x == p1.x:
            py = (p0.y + p1.y) / 2.0
        elif p1.x == l:
            py = p1.y
        elif p0.x == l:
            py = p0.y
            p = p1
        else:
            # use quadratic formula
            z0 = 2.0 * (p0.x - l)
            z1 = 2.0 * (p1.x - l)

            a = 1.0 / z0 - 1.0 / z1
            b = -2.0 * (p0.y / z0 - p1.y / z1)
            c = 1.0 * (p0.y ** 2 + p0.x ** 2 - l ** 2) / z0 - 1.0 * (p1.y ** 2 + p1.x ** 2 - l ** 2) / z1

            py = 1.0 * (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

        px = 1.0 * (p.x ** 2 + (p.y - py) ** 2 - l ** 2) / (2 * p.x - 2 * l)
        res = Point(px, py)
        return res

    def finish_edges(self):
        l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        i = self.arc
        while i.p_next is not None:
            if i.s1 is not None:
                p = self.intersection(i.p, i.p_next.p, l * 2.0)
                i.s1.finish(p)
            i = i.p_next

    def print_output(self):
        it = 0
        for o in self.output:
            it = it + 1
            p0 = o.start
            p1 = o.end
            print(p0.x, p0.y, p1.x, p1.y)

    def get_output(self):
        res = []
        for o in self.output:
            p0 = o.start
            p1 = o.end
            res.append(LineSegment(P(p0.x, p0.y), P(p1.x, p1.y)))
        return res