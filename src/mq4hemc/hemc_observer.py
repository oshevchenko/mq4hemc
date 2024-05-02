from abc import ABC
from threading import RLock

class ObserverM(ABC):
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._observers = []
        cls._mutex = RLock()

    def __init__(self):
        with self._mutex:
            self._observers.append(self)
        self._observables = {}

    def observe(self, msg_id, callback):
        self._observables[msg_id] = callback

    @classmethod
    def clear(cls):
        with cls._mutex:
            for observer in cls._observers:
                observer._observables = {}
            cls._observers = []
        pass

class ObserverEventM(ABC):
    def __init_subclass__(cls, observer_class):
        super().__init_subclass__()
        cls._observer_class = observer_class

    def __init__(self, msg_id, msg_data, autofire=True):
        self.msg_id = msg_id
        self.msg_data = msg_data
        if autofire:
            self.fire()

    def fire(self):
        with self._observer_class._mutex:
            observers = self._observer_class._observers.copy()
        for observer in observers:
            if self.msg_id in observer._observables:
                observer._observables[self.msg_id](self.msg_id, self.msg_data)