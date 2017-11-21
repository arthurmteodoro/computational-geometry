from Representations.Point import Point
from Sets.BinTree import BinTree
from copy import deepcopy


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

    @staticmethod
    def __add_union(root, b):
        if root is None:
            return None
        else:
            Set.__add_union(root.left, b)
            b.insert(root.value)
            Set.__add_union(root.right, b)

    def union(self, b):
        new_set = deepcopy(self)
        Set.__add_union(b.__binTree.get_root(), new_set)
        return new_set

    @staticmethod
    def __add_intersection(root, b, c):
        if root is None:
            return None
        else:
            Set.__add_intersection(root.left, b, c)
            if b.member(root.value):
                c.insert(root.value)
            Set.__add_intersection(root.right, b, c)

    def intersection(self, b):
        new_set = Set()
        Set.__add_intersection(self.__binTree.get_root(), b, new_set)
        return new_set

    @staticmethod
    def __add_difference(root, b, c):
        if root is None:
            return None
        else:
            Set.__add_difference(root.left, b, c)
            if not(b.member(root.value)):
                c.insert(root.value)
            Set.__add_difference(root.right, b, c)

    def difference(self, b):
        new_set = Set()
        Set.__add_difference(self.__binTree.get_root(), b, new_set)
        return new_set


if __name__ == '__main__':
    set1 = Set()
    set2 = Set()

    p1 = Point(1, 2)
    p2 = Point(3, 4)
    p3 = Point(5, 6)
    p4 = Point(7, 8)

    set1.insert(p1)
    set1.insert(p2)
    set1.insert(p3)

    set2.insert(p3)
    set2.insert(p4)

    set3 = set1.union(set2)
    set4 = set1.intersection(set2)
    set5 = set1.difference(set2)
    print("asdasd")
