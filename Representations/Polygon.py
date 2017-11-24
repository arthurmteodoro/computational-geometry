from Sets.Set import Set
from Representations.LineSegment import LineSegment
from Representations.Point import Point


class Polygon:
    def __init__(self):
        self.__segments = Set()
        self.__list_points = []

    def add_segment(self, segment: LineSegment):
        self.__segments.insert(segment)

        exist_in_list_a = False
        exist_in_list_b = False
        for i in self.__list_points:
            if i.comparable(segment.get_a(), i) == 0:
                exist_in_list_a = True
            if i.comparable(segment.get_b(), i) == 0:
                exist_in_list_b = True

        if not exist_in_list_a:
            self.__list_points.append(segment.get_a())
        if not exist_in_list_b:
            self.__list_points.append(segment.get_b())

    def get_num_segments(self):
        return len(self.__segments)

    def get_list_points(self):
        return self.__list_points


if __name__ == '__main__':
    p = Polygon()
    p.add_segment(LineSegment(Point(1, 2), Point(2, 3)))
    p.add_segment(LineSegment(Point(2, 3), Point(5, 6)))
    p.add_segment(LineSegment(Point(5, 6), Point(1, 2)))
