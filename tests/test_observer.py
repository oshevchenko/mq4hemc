import os
import sys
import unittest
from unittest.mock import Mock

# Force insert the path to the beginning of sys.path
# to use the local package instead of the installed package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from mq4hemc import HemcObserver, HemcObserverEvent, HemcMessage

"""
To run this test, run the following commands:
make venv
source ./venv/bin/activate
python3 tests/test_observer.py

To run all unittests from the root directory, run the following command:
make test

To install the package locally, run the following command:
make install
"""

class GNSSObserver(HemcObserver):
    pass

class GNSSObserverEvent(HemcObserverEvent, observer_class=GNSSObserver):
    pass

class AnotherObserver(HemcObserver):
    pass

class AnotherObserverEvent(HemcObserverEvent, observer_class=AnotherObserver):
    pass

class TestObserverEventM(unittest.TestCase):
    def test_init(self):
        mock_process_message = Mock()
        mock_process_message.return_value = "success"

        gnss_observer = GNSSObserver()
        gnss_observer.observe("test_id", mock_process_message)

        msg = HemcMessage()
        msg.type = "test_id"
        GNSSObserverEvent(msg)
        # assert mock_process_message.called_once_with(msg_id, msg_data)
        print(f"gnss_observer._observers: {gnss_observer._observers}")
        mock_process_message1 = Mock()
        mock_process_message1.return_value = "success"

        another_observer = GNSSObserver()
        another_observer.observe("test_id", mock_process_message1)
        msg = HemcMessage()
        msg.type = "test_id"
        GNSSObserverEvent(msg)

        assert 2 == mock_process_message.call_count
        for call in mock_process_message.call_args_list:
            args, kwargs = call
            print(f"Args: {args}, Kwargs: {kwargs}")
            assert args == (HemcMessage(type='test_id', callback=None),)
            # print(f"Args: {args}, Kwargs: {kwargs}")
        assert 1 == mock_process_message1.call_count
        assert mock_process_message1.called_once_with((HemcMessage(type='test_id', callback=None),))

        print(f"gnss_observer._observers: {gnss_observer._observers}")
        print(f"another_observer._observers: {another_observer._observers}")


        # observer_class = MagicMock()
        # observer_class._mutex = MagicMock()
        # observer_class._observers = []

        # event = ObserverEventM(msg_id, msg_data, autofire=False)
        # self.assertEqual(event.msg_id, msg_id)
        # self.assertEqual(event.msg_data, msg_data)

    def test_fire(self):
        import copy

        original = [[1, 2, 3], [4, 5, 6]]
        shallow_copy = copy.copy(original)

        original.append([7, 8, 9])
        original[0][0] = 99

        print(shallow_copy)
if __name__ == "__main__":
    unittest.main()