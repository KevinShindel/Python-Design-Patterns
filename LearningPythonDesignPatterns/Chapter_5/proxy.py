import random
from abc import ABCMeta, abstractmethod


class AbstractObject:
    """ A common interface for the real and proxy objects """
    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, reverse=False):
        """  """
        pass


class RealSubject(AbstractObject):

    def __init__(self):
        self.__digits = [random.random() for _ in range(10000000)]

    def sort(self, reverse=False):
        self.__digits.sort()
        if reverse:
            self.__digits.reverse()


class Proxy(AbstractObject):
    reference_cnt = 0
    __cached_object = None

    def __init__(self):
        if not getattr(self.__class__, '__cached_object', None):
            self.__cached_object = RealSubject()
            print('Create new instance of RealSubject')
        else:
            print('Use existing instance RealSubject')

        self.__class__.reference_cnt += 1
        print('Count of references: ', self.__class__.reference_cnt)

    def sort(self, reverse=False):
        self.__cached_object.sort(reverse=reverse)

    def __del__(self):
        self.__class__.reference_cnt -= 1
        if self.__class__.reference_cnt == 0:
            del self.__class__.__cached_object
            print('Number of references objects is 0. Deleting cached object')

        print('Deleted object. Count of objects: ', self.__class__.reference_cnt)


if __name__ == '__main__':
    proxy1 = Proxy()
    proxy2 = Proxy()
    proxy3 = Proxy()

    proxy1.sort(True)
    del proxy2

    exit(0)
