import threading
from dataclasses import dataclass
import queue
from typing import Any


@dataclass
class HemcMessage:
    """
    Represents a message for the HEMC system.

    Attributes:
        type (str): The type of the message.
        callback (callable): The callback function to be executed when the message is received.
    """
    type: str = 'default_msg_type'
    callback: callable = None


class HemcQueue(queue.Queue):
    """
    A custom queue class that extends the `queue.Queue` class.
    This class provides an additional method `get_process` that allows processing of items before returning them.

    Args:
        process_item_cb (callable, optional): A callable function that will be used to process each item retrieved from the queue.

    Attributes:
        _process_item_cb (callable): The function used to process each item.

    """

    def __init__(self, process_item_cb: callable = None):
        self._process_item_cb = process_item_cb
        super().__init__()

    @property
    def process_item_cb(self):
        return self._process_item_cb

    @process_item_cb.setter
    def process_item_cb(self, value):
        if not callable(value):
            raise ValueError("process_item_cb must be a callable function!")
        self._process_item = value

    def get_process(self, block=True, timeout=None):
        """
        Retrieves and processes an item from the queue.

        Args:
            block (bool, optional): If True (default), the method will block until an item is available.
            timeout (float, optional): The maximum time to wait for an item to become available.

        Returns:
            item: The retrieved item from the queue.

        """
        item = super().get(block, timeout)

        if callable(self._process_item_cb):
            ret = self._process_item_cb(item)
        if isinstance(item, HemcMessage) and item.callback:
            item.callback(ret)
        return item


class HemcQueueSender():
    """
    A class representing a sender for a HemcQueue.

    Attributes:
        _mq (HemcQueue): The HemcQueue object to send messages to.
        _condition (threading.Condition): A threading.Condition object for synchronization.
        _status (Any): The status received from the callback function.

    Methods:
        get_status_wrapper(status: Any) -> None:
            A callback function to receive the status from the message.

        send_wait_reply(message: HemcMessage) -> Any:
            Sends a message to the HemcQueue and waits for a reply.
            Returns the status received from the callback function.

        send(message: HemcMessage) -> None:
            Sends a message to the HemcQueue without waiting for a reply.
    """

    def __init__(self, mq: HemcQueue):
        self._mq = mq
        self._condition = threading.Condition()
        self._status = None

    def get_status_wrapper(self, status: Any) -> None:
        """
        A callback function to receive the status from the message.

        Args:
            status (Any): The status received from the message.
        """
        with self._condition:
            self._status = status
            self._condition.notify()

    def send_wait_reply(self, message: HemcMessage) -> Any:
        """
        Sends a message to the HemcQueue and waits for a reply.

        Args:
            message (HemcMessage): The message to send.

        Returns:
            Any: The status received from the callback function.
        """
        message.callback = self.get_status_wrapper
        with self._condition:
            self._mq.put(message)
            self._condition.wait()
        return self._status

    def send(self, message: HemcMessage) -> None:
        """
        Sends a message to the HemcQueue without waiting for a reply.

        Args:
            message (HemcMessage): The message to send.
        """
        message.callback = None
        self._mq.put(message)
