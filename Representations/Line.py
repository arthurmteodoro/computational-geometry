from Representations.Element import Element
from Representations.Point import Point


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

    @staticmethod
    def generate_by_two_points(a: Point, b: Point):
        matrix = [[0 for x in range(5)] for x in range(3)]

        matrix[0] = [1, 1, 1, 1, 1]
        matrix[1][2] = 1
        matrix[2][2] = 1

        matrix[1][0] = a.get_x()
        matrix[1][1] = a.get_y()
        matrix[1][3] = a.get_x()
        matrix[1][4] = a.get_y()

        matrix[2][0] = b.get_x()
        matrix[2][1] = b.get_y()
        matrix[2][3] = b.get_x()
        matrix[2][4] = b.get_y()

        diagonal1 = [0, 0, 0]
        diagonal1[0] = matrix[0][0] * matrix[1][1] * matrix[2][2]
        diagonal1[1] = matrix[0][1] * matrix[1][2] * matrix[2][3]
        diagonal1[2] = matrix[0][2] * matrix[1][3] * matrix[2][4]

        diagonal2 = [0, 0, 0]
        diagonal2[0] = matrix[2][0] * matrix[1][1] * matrix[0][2]
        diagonal2[1] = matrix[2][1] * matrix[1][2] * matrix[0][3]
        diagonal2[2] = matrix[2][2] * matrix[1][3] * matrix[0][4]

        eq = [0, 0, 0]
        eq[0] = diagonal1[0] - diagonal2[1]
        eq[1] = diagonal1[1] - diagonal2[2]
        eq[2] = diagonal1[2] - diagonal2[0]

        return Line(eq[0], eq[1], eq[2])

    def get_y_from_x(self, x):
        value_x = self.get_a()*x
        value_first_term = value_x + self.get_c()
        value_second_term = -self.get_b()

        return value_first_term/value_second_term

    def get_x_from_y(self, y):
        value_y = self.get_b()*y
        value_first_term = value_y + self.get_c()
        value_second_term = -self.get_a()

        return value_first_term/value_second_term


if __name__ == '__main__':
    a = Point(1, 1)
    b = Point(4, 6)

    line = Line.generate_by_two_points(a, b)
    print(line.get_y_from_x(4))

    print(line.get_x_from_y(6))
