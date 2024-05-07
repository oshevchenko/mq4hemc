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
from mq4hemc import HemcMessage, HemcService, HemcObserver, HemcObserverEvent, HemcTick

import threading

"""
To run this test, run the following commands:
make venv
source ./venv/bin/activate
python3 tests/test_readme.py
"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('test_mq4hemc')


class TickObserver(HemcObserver):
    pass


class TickObserverEvent(HemcObserverEvent, observer_class=TickObserver):
    pass


@dataclass
class BigHemcMessage(HemcMessage):
    payload: dict = field(default_factory=dict)


def process_cb(item: HemcMessage):
    if hasattr(item, 'payload') and item.payload is not None:
        # Simulate processing time
        time.sleep(1)
    logger.info(f"Processed message '{item.type}'")
    return item.type


service = HemcService(process_cb)


def process_tick(item: HemcMessage):
    logger.info(f"Processed tick message '{item.type}'")
    ret = service.send_sync_msg(item)
    return ret


def timer_tick():
    print("Timer executed!")
    msg = BigHemcMessage()
    msg.type = "tick"
    msg.payload = {"key": "value"}
    # TickObserverEvent(HemcMessage(type="tick"))
    ret_dict = {}
    TickObserverEvent(msg, ret_dict)
    print(f"ret_dict: {ret_dict}")


if __name__ == "__main__":
    tick_sender = HemcTick(5, timer_tick)
    # Create a timer that waits for 5 seconds, then executes timer_tick
    tick_observer = TickObserver(name="main_tick_observer")
    tick_observer.observe("tick", process_tick)

    tick_observer1 = TickObserver(name="main_tick_observer1")
    tick_observer1.observe("tick", process_tick)

    # Start the timer
    service.start()
    tick_sender.start()

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
    time.sleep(10)
    service.stop()
    service.join()
    logger.info("Service stopped.")
