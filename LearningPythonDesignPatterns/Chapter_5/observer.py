import datetime
import time
from typing import List
from abc import ABCMeta, abstractmethod


class Observer:
    """ Abstract class for observers , provides notify method as interface for subjects"""

    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def notify(self, timestamp):
        pass


class USATimeObserver(Observer):

    def notify(self, timestamp):
        time_msg = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %I:%M:%S%p')
        print('Observer: ', self.name, ' says: ', time_msg)


class EUTimeObserver(Observer):

    def notify(self, timestamp):
        time_msg = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %I:%M:%S')
        print('Observer: ', self.name, ' says: ', time_msg)


class Producer:

    def __init__(self):
        self.__observers: List[Observer] = []
        self.cur_time = None

    def register_observer(self, observer: Observer):
        if observer not in self.__observers:
            self.__observers.append(observer)
            print('Register new observer: ', observer.name)
        else:
            print('Observer already exists')

    def unregister_observer(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)
            print('Observer: ', observer.name, ' has been removed.')

        else:
            print('Observer is not found!')

    def notify_observers(self):
        print('Notify all Observers')
        self.cur_time = time.time()
        for observer in self.__observers:
            observer.notify(self.cur_time)


if __name__ == '__main__':
    producer = Producer()
    observer1 = USATimeObserver('usa_time_observer')
    observer2 = USATimeObserver('eu_time_observer')

    time.sleep(1)
    producer.register_observer(observer1)
    producer.notify_observers()
    time.sleep(1)

    producer.register_observer(observer2)
    producer.notify_observers()

    time.sleep(1)
    producer.unregister_observer(observer1)
    producer.notify_observers()

    exit(0)
