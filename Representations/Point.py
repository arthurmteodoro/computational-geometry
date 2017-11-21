from Representations.Element import Element


class Point(Element):
    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    @staticmethod
    def comparable(obj1, obj2):
        obj1 = obj1.get_x() + obj1.get_y()
        obj2 = obj2.get_x() + obj2.get_y()

        if obj2 > obj1:
            return 1
        elif obj2 == obj1:
            return 0
        else:
            return -1
