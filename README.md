# Message Queue Based Service
```py
from mq4hemc import HemcMessage, HemcService
```
`HemcService` - a class to create a separate thread which is extracting messages
from the message queue and passes them to user callback for processing.
It has a thread-safe methods to add messages to the queue synchronously
(wait until processed) and asynchronously.


`HemcMessage` - a dataclass to inherit from to create a custom message.

## Example of usage
Define a custom class for the messages:
```py
@dataclass
class BigHemcMessage(HemcMessage):
    payload: dict = field(default_factory=dict)
```
Create a service which is running in a separate thread and processes
messages from the message queue:
```py
service = HemcService()
```
Register a callback function to process messages from the message queue:
```py
def process_cb(item: HemcMessage):
    if hasattr(item, 'payload') and item.payload is not None:
        # Simulate processing time
        time.sleep(1)
    logger.info(f"Processed message '{item.type}', payload: {item.payload}")
    return item.type

service.register_process_cb(process_cb)
```
A callback method could also be passed to the constructor:
```py
service = HemcService(process_cb)
```
Start a service:
```py
service.start()
```
Send messages from another thread asynchronously (without waiting until the message is processed)
```py
for i in range(3):
    message = BigHemcMessage()
    message.type = f"test{i}"
    message.payload = {"key": f"value{i}"}
    logger.info(f"Send {message.type} and do not wait for reply.")
    status = service.send_async_msg(message)
```
Send a message from another thread  synchronously (wait until the message is processed) and get the response from callback method.
```py
message = BigHemcMessage()
message.type = "test_sync"
message.payload = {"key": "value"}
logger.info(f"Now send {message.type} and wait for reply...")
status = service.send_sync_msg(message)
logger.info(f"Message {message.type} processed, reply: {status}")
```
Stop the service.
```py
service.stop()
service.join()
logger.info("Service stopped.")
```
This code will produce the following output. Please pay attention to the **test_sync** timestamps.
```
2024-05-02 14:39:28 - test_mq4hemc - INFO - Send test0 and do not wait for reply.
2024-05-02 14:39:28 - test_mq4hemc - INFO - Send test1 and do not wait for reply.
2024-05-02 14:39:28 - test_mq4hemc - INFO - Send test2 and do not wait for reply.
2024-05-02 14:39:28 - test_mq4hemc - INFO - Now send test_sync and wait for reply...
2024-05-02 14:39:29 - test_mq4hemc - INFO - Processed message 'test0'
2024-05-02 14:39:30 - test_mq4hemc - INFO - Processed message 'test1'
2024-05-02 14:39:31 - test_mq4hemc - INFO - Processed message 'test2'
2024-05-02 14:39:32 - test_mq4hemc - INFO - Processed message 'test_sync'
2024-05-02 14:39:32 - test_mq4hemc - INFO - Message test_sync processed, reply: test_sync
2024-05-02 14:39:32 - test_mq4hemc - INFO - Service stopped.
```
