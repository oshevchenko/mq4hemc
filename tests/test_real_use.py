import threading
import os
import sys
from dataclasses import dataclass, field
import logging
import time
import unittest
from unittest.mock import Mock

# Force insert the path to the beginning of sys.path
# to use the local package instead of the installed package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from mq4hemc import HemcMessage, HemcService

"""
To run this test, run the following commands:
make venv
source ./venv/bin/activate
python3 tests/test_real_use.py

To run all unittests from the root directory, run the following command:
make test

To install the package locally, run the following command:
make install
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test_mq4hemc')

@dataclass
class BigHemcMessage(HemcMessage):
    payload: dict = field(default_factory=dict)

class TestHemcService(unittest.TestCase):
    def test_send_wait_reply(self):
        mock_process_message = Mock()
        mock_process_message.return_value = "__success__"

        service = HemcService(mock_process_message)
        service.start()

        for i in range(3):
            message = BigHemcMessage()
            message.type = f"test{i}"
            message.payload = {"key": f"value{i}"}
            logger.info(f"Send {message} and do not wait for reply.")
            status = service.send_async_msg(message)


        message = BigHemcMessage()
        message.type = "test_sync"
        message.payload = {"key": "value"}
        logger.info(f"Now send {message} and wait for reply...")
        status = service.send_sync_msg(message)
        logger.info(f"Message {message} processed, reply: {status}")
        service.stop()
        service.join()
        for call in mock_process_message.call_args_list:
            print(f"Called with args: {call.args}, kwargs: {call.kwargs}")
        assert mock_process_message.call_count == 4
        call_1 = mock_process_message.call_args_list[0]
        assert call_1[0][0].type == "test0"
        assert call_1[0][0].payload == {"key": "value0"}
        call_2 = mock_process_message.call_args_list[1]
        assert call_2[0][0].type == "test1"
        assert call_2[0][0].payload == {"key": "value1"}
        call_3 = mock_process_message.call_args_list[2]
        assert call_3[0][0].type == "test2"
        assert call_3[0][0].payload == {"key": "value2"}
        call_4 = mock_process_message.call_args_list[3]
        assert call_4[0][0].type == "test_sync"
        assert call_4[0][0].payload == {"key": "value"}
        assert status == "__success__"


if __name__ == "__main__":
    unittest.main()
    """
    def process_cb(item: HemcMessage):
        if hasattr(item, 'payload') and item.payload is not None:
            # Simulate processing time
            time.sleep(1)
        logger.info(f"Processed message '{item.type}', payload: {item.payload}")
        return item.type

    service = HemcService(process_cb)
    service.start()

    for i in range(3):
        message = BigHemcMessage()
        message.type = f"test{i}"
        message.payload = {"key": f"value{i}"}
        logger.info(f"Send {message} and do not wait for reply.")
        status = service.send_async_msg(message)

    message = BigHemcMessage()
    message.type = "test_sync"
    message.payload = {"key": "value"}
    logger.info(f"Now send {message} and wait for reply...")
    status = service.send_sync_msg(message)
    logger.info(f"Message {message} processed, reply: {status}")
    service.stop()
    service.join()
    logger.info("Service stopped.")
    """
