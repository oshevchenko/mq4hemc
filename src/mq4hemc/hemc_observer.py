from abc import ABC
from threading import RLock
from mq4hemc import HemcQueue, HemcQueueSender, HemcMessage


class HemcObserver(ABC):
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._observers = []
        cls._mutex = RLock()

    def __init__(self):
        with self._mutex:
            self._observers.append(self)
        self._observables = {}

    def get_observables(self):
        with self._mutex:
            observables = self._observables.copy()
        return observables

    def observe(self, msg_id, callback):
        if not callable(callback):
            raise ValueError("callback must be a callable function or method")
        with self._mutex:
            self._observables[msg_id] = callback

    @classmethod
    def fire(cls, msg: HemcMessage):
        with cls._mutex:
            observers = cls._observers.copy()
        for observer in observers:
            observables = observer.get_observables()
            if msg.type in observables:
                callback = observables[msg.type]
                callback(msg)

    @classmethod
    def clear(cls):
        for observer in cls._observers:
            observer.observables.clear()
        cls._observers.clear()


class HemcObserverEvent(ABC):
    def __init_subclass__(cls, observer_class):
        super().__init_subclass__()
        if not issubclass(observer_class, HemcObserver):
            raise TypeError("observer_class must be a subclass of HemcObserver")
        cls._observer_class = observer_class

    def __init__(self, msg: HemcMessage, autofire=True):
        self.msg = msg
        if autofire:
            self.fire()

    def fire(self):
        self._observer_class.fire(self.msg)
