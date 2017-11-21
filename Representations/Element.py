from abc import ABCMeta, abstractmethod


class Element(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def comparable(obj1, obj2):
        pass
