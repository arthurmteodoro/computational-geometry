from Representations.Element import Element


class Circle(Element):
    def __init__(self, centre=None, radius=0):
        self.__centre = centre
        self.__radius = radius

    def get_centre(self):
        return self.__centre

    def get_radius(self):
        return self.__radius

    def set_centre(self, centre):
        self.__centre = centre

    def set__radius(self, radius):
        self.__radius = radius

    @staticmethod
    def comparable(obj1, obj2):
        if obj2.get_radius() > obj1.get_radius():
            return 1
        elif obj1.get_radius() == obj2.get_radius():
            return 0
        else:
            return -1
