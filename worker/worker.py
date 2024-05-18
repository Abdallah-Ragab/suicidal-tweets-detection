import json
import os
import pika
from queue import TaskQueue, QueueConnection
from scraper.scraper import Scraper
from analyzer.analyzer import Analyzer
import logging

logger = logging.getLogger()

TASK_QUEUE_NAME = "tasks"
TAST_STATUS_MAP = json.loads(open("task_status.json").read())


class Worker:
    received_task = {}

    def __init__(self):
        logger.info("Initializing worker...")
        self.connection = QueueConnection()
        self.queue = TaskQueue(self.connection, TASK_QUEUE_NAME, self.callback)
        self.scraper = Scraper(20)
        self.analyzer = Analyzer()
        self.ready()

    def callback(self, ch, method, properties, body):
        self.received_task = {"channel": ch, "method": method, "properties": properties, "body": body}
        logger.info(f"Received task: {body.decode()}")
        self.do()
        self.done()

    def ready(self):
        self.queue.listen()

    def done(self):
        self.received_task["channel"].basic_ack(delivery_tag=self.received_task["method"].delivery_tag)

    def do(self):
        username = self.received_task["body"].decode()
        print(f"Received task: {task_data}")
        print(self.scrape(username))

    def scrape(self, username):
        return self.scraper.tweets(username)





class Task:
    def __init__(self):
        self.status = TAST_STATUS_MAP["created"]
        self.data = {
            "user": None,
            "tweets": None,
            "analysis": None,
        }
