from Representations.Point import Point
import math


def distance_between_two_points(pa: Point,pb: Point):
    return math.sqrt(pow(pb.get_x() - pa.get_x(), 2) + pow(pb.get_y() - pa.get_y(), 2))
