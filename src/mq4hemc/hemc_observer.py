from abc import ABC
from threading import RLock
from mq4hemc import HemcQueue, HemcQueueSender, HemcMessage


class HemcObserver(ABC):
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._ret_dict = {}
        cls._observers = []

    def __init__(self, name: str = "default"):
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        self.name = name
        self._observables = {}
        self._observers.append(self)

    def get_observables_copy(self):
        observables = self._observables.copy()
        return observables

    def observe(self, msg_id, callback):
        if not isinstance(msg_id, str):
            raise ValueError("msg_id must be a string")
        if not callable(callback):
            raise ValueError("callback must be a callable function or method")
        self._observables[msg_id] = callback

    @classmethod
    def fire(cls, msg: HemcMessage, ret_dict: dict = None):
        cls._ret_dict.clear()
        observers = cls._observers.copy()
        for observer in observers:
            observables = observer.get_observables_copy()
            if msg.type in observables:
                callback = observables[msg.type]
                print(f"observer.name: {observer.name}")
                cls._ret_dict[observer.name] = callback(msg)
        if ret_dict is not None:
            ret_dict.update(cls._ret_dict)

    @classmethod
    def clear(cls):
        for observer in cls._observers:
            observer._observables.clear()
        cls._observers.clear()


class HemcObserverEvent(ABC):
    def __init_subclass__(cls, observer_class: HemcObserver):
        super().__init_subclass__()
        if not issubclass(observer_class, HemcObserver):
            raise TypeError("observer_class must be a subclass of HemcObserver")
        cls._observer_class = observer_class

    def __init__(self, msg: HemcMessage, ret_dict: dict = None, autofire: bool = True):
        self.msg = msg
        if autofire:
            self.fire(ret_dict)

    def fire(self, ret_dict: dict = None):
        self._observer_class.fire(self.msg, ret_dict=ret_dict)
