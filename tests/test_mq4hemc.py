import threading
import os
import sys
import unittest
from unittest.mock import Mock
import logging
from dataclasses import dataclass, field

# Force insert the path to the beginning of sys.path
# to use the local package instead of the installed package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from mq4hemc import HemcQueue, HemcQueueSender, HemcMessage

"""
To run this test, run the following commands:
make venv
source ./venv/bin/activate
python3 tests/test_mq4hemc.py

To run all unittests from the root directory, run the following command:
make test

To install the package locally, run the following command:
make install
"""

@dataclass
class BigHemcMessage(HemcMessage):
    payload: dict = field(default_factory=dict)

class TestMq4Hemc(unittest.TestCase):
    def test_send_wait_reply(self):
        mock_process_message = Mock()
        mock_process_message.return_value = "success"

        queue = HemcQueue(process_item_cb = mock_process_message)
        test_thread = threading.Thread(target=queue.get_process, args=(True,))
        test_thread.start()

        sender = HemcQueueSender(queue)
        message = HemcMessage()
        message.type = "test1"
        # the return value of send_wait_reply() is the return value of HemcQueue.process_item_cb()
        status = sender.send_wait_reply(message)
        # Wait for return from queue.get_process()
        test_thread.join()
        mock_process_message.assert_called_once()
        item = mock_process_message.call_args[0][0]
        assert isinstance(item, HemcMessage)
        assert status == "success"
        assert item.callback == sender.get_status_wrapper
        assert item.type == "test1"

    def test_send_wait_reply_big(self):
        mock_process_message = Mock()
        mock_process_message.return_value = "success"

        queue = HemcQueue(process_item_cb = mock_process_message)
        test_thread = threading.Thread(target=queue.get_process, args=(True,))
        test_thread.start()

        sender = HemcQueueSender(queue)
        message = BigHemcMessage()
        message.type = "test1"
        message.payload = {"key": "value"}
        # the return value of send_wait_reply() is the return value of HemcQueue.process_item_cb()
        status = sender.send_wait_reply(message)
        # Wait for return from queue.get_process()
        test_thread.join()
        mock_process_message.assert_called_once()
        item = mock_process_message.call_args[0][0]
        assert isinstance(item, HemcMessage)
        assert status == "success"
        assert item.callback == sender.get_status_wrapper
        assert item.type == "test1"
        assert item.payload == {"key": "value"}

    def test_send(self):
        mock_process_message = Mock()
        mock_process_message.return_value = "success"

        queue = HemcQueue(process_item_cb = mock_process_message)
        test_thread = threading.Thread(target=queue.get_process, args=(True,))
        test_thread.start()

        sender = HemcQueueSender(queue)
        # As we use 'send' method, the callback should not be called.
        sender.get_status_wrapper = Mock()
        message = HemcMessage()
        message.type = "test2"
        sender.send(message)
        # Wait for return from queue.get_process()
        test_thread.join()

        sender.get_status_wrapper.assert_not_called()
        mock_process_message.assert_called_once()
        item = mock_process_message.call_args[0][0]
        assert isinstance(item, HemcMessage)
        assert item.type == "test2"

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger('test_mq4hemc')

    unittest.main()
