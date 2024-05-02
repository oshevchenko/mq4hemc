import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from unittest.mock import MagicMock
from mq4hemc import ObserverM, ObserverEventM

"""
To run this test, run the following commands:

python3 -m venv ./venv
source ./venv/bin/activate
python3 tests/test_mq4hemc.py

To run all unittests from the root directory, run the following command:
python3 -m unittest discover -s tests

To install the package locally, run the following command:

python3 -m pip install .

"""

class GNSSObserver(ObserverM):
    pass

class GNSSObserverEvent(ObserverEventM, observer_class=GNSSObserver):
    pass

class AnotherObserver(ObserverM):
    pass

class AnotherObserverEvent(ObserverEventM, observer_class=AnotherObserver):
    pass

class TestObserverEventM(unittest.TestCase):
    def test_init(self):
        mock_process_message = unittest.mock.Mock()
        mock_process_message.return_value = "success"

        gnss_observer = GNSSObserver()
        gnss_observer.observe("test_id", mock_process_message)

        msg_id = "test_id"
        msg_data = "test_data"
        GNSSObserverEvent(msg_id, msg_data)
        # assert mock_process_message.called_once_with(msg_id, msg_data)
        print(f"gnss_observer._observers: {gnss_observer._observers}")
        mock_process_message1 = unittest.mock.Mock()
        mock_process_message1.return_value = "success"

        another_observer = GNSSObserver()
        another_observer.observe("test_id", mock_process_message1)
        msg_id = "test_id"
        msg_data = "test_data"
        # AnotherObserverEvent(msg_id, msg_data)
        GNSSObserverEvent(msg_id, msg_data)

        assert 2 == mock_process_message.call_count
        for call in mock_process_message.call_args_list:
            args, kwargs = call
            assert args == ('test_id', 'test_data')
            # print(f"Args: {args}, Kwargs: {kwargs}")
        assert 1 == mock_process_message1.call_count
        assert mock_process_message1.called_once_with(msg_id, msg_data)

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