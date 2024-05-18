import json
import os
import pika
from queue import TaskQueue, QueueConnection
from scraper.scraper import Scraper
from analyzer.analyzer import Analyzer
import logging

logger = logging.getLogger()

TASK_QUEUE_NAME = "tasks"
TASK_STATUS_MAP = json.loads(open("task_status.json").read())


class Task:
    def __init__(self, status=None, data=None):
        self.status = status or TASK_STATUS_MAP["created"]
        self.data = data or {
            "user": None,
            "tweets": None,
            "analysis": None,
        }
    def set_status(self, status_str):
        self.status = TASK_STATUS_MAP.get(status_str, TASK_STATUS_MAP["created"])

    def serialize(self):
        return json.dumps({
            "status": self.status,
            "data": self.data,
        })

    def deserialize(self, data):
        data = json.loads(data)
        self.status = data["status"]
        self.data = data["data"]


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
        self.task = Task()
        logger.info(f"Received task: {body.decode()}")
        self.do()
        self.done()

    def ready(self):
        self.queue.listen()

    def done(self):
        self.received_task["channel"].basic_ack(delivery_tag=self.received_task["method"].delivery_tag)

    def do(self):
        username = self.received_task["body"].decode()
        print(f"Received task: {username}")
        print(self.scrape(username))

    def scrape(self, username):
        logger.info(f"Scraping {username}...")
        result = self.scraper.tweets(username)
        if result:
            self.task.data["user"] = username
            self.task.data["tweets"] = result
            self.task.set_status("scraped")
            return result
        return




