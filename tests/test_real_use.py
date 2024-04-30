import threading
from mq4hemc import HemcQueue, HemcQueueSender, HemcMessage
from dataclasses import dataclass, field
import logging

@dataclass
class BigHemcMessage(HemcMessage):
    payload: dict = field(default_factory=dict)


class TestService(threading.Thread):
    def start(self) -> None:
        if self._running:
            return
        self._running = True
        return super().start()

    def stop(self):
        self._running = False
        message = HemcMessage()
        message.type = "stop"
        self.get_sender().send(message)

    def process_item(self, item: HemcMessage):
        if hasattr(item, 'payload') and item.payload is not None:
            print(f"Processing message '{item.type}', payload: {item.payload}")
        return item.type

    def __init__(self):
        # Initialize the message queue
        self.message_queue = HemcQueue(process_item_cb = self.process_item)
        self._running = False
        threading.Thread.__init__(self)

    def get_sender(self):
        return HemcQueueSender(self.message_queue)

    def run(self):
        # The main execution loop of the thread.
        while self._running:
            # Get message from the queue and process it
            self.message_queue.get_process()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger('test_mq4hemc')
    service = TestService()
    service.start()
    message = BigHemcMessage()
    message.type = "test1"
    message.payload = {"key": "value"}
    # the return value of send_wait_reply() is the return value of HemcQueue.process_item_cb()
    sender = service.get_sender()
    status = sender.send_wait_reply(message)
    print(f"Status: {status}")
    service.stop()
    service.join()

