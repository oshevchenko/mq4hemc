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
python3 tests/test_readme.py
"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('test_mq4hemc')


@dataclass
class BigHemcMessage(HemcMessage):
    payload: dict = field(default_factory=dict)


if __name__ == "__main__":
    def process_cb(item: HemcMessage):
        if hasattr(item, 'payload') and item.payload is not None:
            # Simulate processing time
            time.sleep(1)
        logger.info(f"Processed message '{item.type}'")
        return item.type

    service = HemcService(process_cb)
    service.start()

    for i in range(3):
        message = BigHemcMessage()
        message.type = f"test{i}"
        message.payload = {"key": f"value{i}"}
        logger.info(f"Send {message.type} and do not wait for reply.")
        status = service.send_async_msg(message)

    message = BigHemcMessage()
    message.type = "test_sync"
    message.payload = {"key": "value"}
    logger.info(f"Now send {message.type} and wait for reply...")
    status = service.send_sync_msg(message)
    logger.info(f"Message {message.type} processed, reply: {status}")
    service.stop()
    service.join()
    logger.info("Service stopped.")
