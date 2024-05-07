from threading import Timer

class HemcTick:
    def __init__(self, interval, callback_tick):
        if not isinstance(interval, (int, float)):
            raise ValueError("interval must be a number")
        self.interval = interval
        if not callable(callback_tick):
            raise ValueError("callback_tick must be a callable function or method")
        self.callback = callback_tick
        self.timer = None

    def start(self):
        self.timer = Timer(self.interval, self.send_tick_event)
        self.timer.daemon = True
        self.timer.start()

    def send_tick_event(self):
        self.callback()
        self.start()
