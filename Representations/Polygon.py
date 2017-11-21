from Sets.Set import Set
from Representations import LineSegment


class Polygon:
    def __init__(self):
        self.__segments = Set()

    def add_segment(self, segment: LineSegment):
        self.__segments.insert(segment)
