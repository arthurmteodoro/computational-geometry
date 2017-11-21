from Representations.Element import Element
import math


class LineSegment(Element):
    def __init__(self, a=None, b=None):
        self.__pointA = a
        self.__pointB = b

    def set_a(self, a):
        self.__pointA = a

    def set_b(self, b):
        self.__pointA = b

    def get_a(self):
        return self.__pointA

    def get_b(self):
        return self.__pointB

    @staticmethod
    def comparable(obj1, obj2):
        tam_obj1 = math.sqrt(pow(obj1.get_b().get_x() - obj1.get_a().get_x(), 2)
                             + pow(obj1.get_b().get_y() - obj1.get_a().get_y(), 2))
        tam_obj2 = math.sqrt(pow(obj2.get_b().get_x() - obj2.get_a().get_x(), 2)
                             + pow(obj2.get_b().get_y() - obj2.get_a().get_y(), 2))

        if tam_obj2 > tam_obj1:
            return 1
        elif obj1.get_a().get_x() == obj2.get_a().get_x() and obj1.get_a().get_y() == obj2.get_a().get_x() and \
                obj1.get_b().get_x() == obj2.get_b().get_x() and obj1.get_b().get_y() == obj2.get_b().get_x():
            return 0
        else:
            return -1
