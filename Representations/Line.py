from Representations.Element import Element


class Line(Element):
    def __init__(self, a=0, b=0, c=0):
        self.__a = a
        self.__b = b
        self.__c = c

    def get_a(self):
        return self.__a

    def get_b(self):
        return self.__b

    def get_c(self):
        return self.__c

    def set_a(self, a):
        self.__a = a

    def set_b(self, b):
        self.__b = b

    def set_c(self, c):
        self.__c = c

    @staticmethod
    def comparable(obj1, obj2):
        sum1 = obj1.get_a() + obj1.get_b() + obj1.get_c()
        sum2 = obj2.get_a() + obj2.get_b() + obj2.get_c()

        if sum2 > sum1:
            return 1
        elif obj1.get_a() == obj2.get_a() and obj1.get_b() == obj2.get_b() and obj1.get_c() == obj2.get_c():
            return 0
        else:
            return -1
