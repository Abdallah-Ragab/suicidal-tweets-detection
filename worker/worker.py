import json
import os
import pika
from queue import TaskQueue, QueueConnection

TASK_QUEUE_NAME = "tasks"
TAST_STATUS_MAP = json.loads(open("task_status.json").read())


class Worker:
    received_task = {}

    def __init__(self):
        self.connection = QueueConnection()
        self.queue = TaskQueue(self.connection, TASK_QUEUE_NAME, self.callback)
        self.ready()

    def callback(self, ch, method, properties, body):
        self.received_task = {"channel": ch, "method": method, "properties": properties, "body": body}
        self.do()
        self.done()

    def ready(self):
        self.queue.listen()

    def done(self):
        self.received_task["channel"].basic_ack(delivery_tag=self.received_task["method"].delivery_tag)

    def do(self):
        task_data = self.received_task["body"].decode()
        print(f"Received task: {task_data}")




class Task:
    def __init__(self):
        self.status = TAST_STATUS_MAP["created"]
        self.data = {
            "user": None,
            "tweets": None,
            "analysis": None,
        }
