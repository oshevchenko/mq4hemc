import threading
from mq4hemc import HemcQueue, HemcQueueSender, HemcMessage

class HemcService(threading.Thread):
    def __init__(self, process_cb = None):
        # Initialize the message queue
        self._message_queue = HemcQueue(process_item_cb = self._process_item)
        self._running = False
        self._process_cb = None
        if process_cb is not None:
            if not callable(process_cb):
                raise ValueError("process_cb must be a callable function!")
            self._process_cb = process_cb
        threading.Thread.__init__(self)


    def _process_item(self, item: HemcMessage):
        ret = None
        if item.type != "__stop__" and self._process_cb is not None:
            ret = self._process_cb(item)
        return ret


    def _get_sender(self):
        return HemcQueueSender(self._message_queue)


    def start(self) -> None:
        if self._running:
            return
        self._running = True
        return super().start()


    def send_sync_msg(self, message: HemcMessage):
        return self._get_sender().send_wait_reply(message)


    def send_async_msg(self, message: HemcMessage):
        return self._get_sender().send(message)


    def stop(self):
        self._running = False
        message = HemcMessage()
        message.type = "__stop__"
        self.send_async_msg(message)


    def register_process_cb(self, process_cb):
        if not callable(process_cb):
            raise ValueError("process_cb must be a callable function!")
        self._process_cb = process_cb


    def run(self):
        # The main execution loop of the thread.
        while self._running:
            # Get message from the queue and process it
            self._message_queue.get_process()
