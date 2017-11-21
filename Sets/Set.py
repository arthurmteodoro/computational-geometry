from Representations.Point import Point
from Sets.BinTree import BinTree


class Set:
    def __init__(self):
        self.__binTree = BinTree()

    def member(self, value):
        try:
            return True if self.__binTree.search(value, value.comparable) else False
        except AttributeError:
            return True if self.__binTree.search(value) else False

    def insert(self, value):
        try:
            self.__binTree.insert(value, value.comparable)
        except AttributeError:
            self.__binTree.insert(value)

    def delete(self, value):
        self.__binTree.delete(value, value.comparable)

    @staticmethod
    def __search_in_set(root, value):
        if root is None:
            return None
        else:
            b = None
            a = Set.__search_in_set(root.left, value)
            if root.value.member(value):
                b = root.value
            c = Set.__search_in_set(root.right, value)

            return a or b or c

    def find(self, value):
        root = self.__binTree.get_root()
        return Set.__search_in_set(root, value)


if __name__ == '__main__':
    set1 = Set()
    set2 = Set()
    set3 = Set()
    set4 = Set()

    p1 = Point(1, 2)
    p2 = Point(3, 4)
    p3 = Point(5, 6)
    p4 = Point(7, 8)
    p5 = Point(9, 10)
    p6 = Point(11, 12)

    set1.insert(p1)
    set1.insert(p2)
    set1.insert(p1)

    set2.insert(p3)
    set2.insert(p4)

    set3.insert(p5)
    set3.insert(p6)

    set4.insert(set1)
    set4.insert(set2)
    set4.insert(set3)
    print("asd")

    p7 = set4.find(p3)
    print(p7)
    print("asdasd")
