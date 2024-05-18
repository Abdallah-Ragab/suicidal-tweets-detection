import json
import os
import pika
from tqueue import TaskQueue, QueueConnection
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
            "message": None,
            "result": None,
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
        self.scraper = Scraper(5)
        self.analyzer = Analyzer()
        self.ready()

    def callback(self, ch, method, properties, body):
        self.received_task = {"channel": ch, "method": method, "properties": properties, "body": body}
        self.task = Task()
        self.task.set_status("scheduled")
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
        print(f"Scraped {username}. result: {self.scrape(username)}")
        print(f"Analyzed {username}. result: {self.analyze()}")
        print(f"Result: {self.result()}")
        print(f"Task status: {self.task.serialize()}")

    def scrape(self, username):
        logger.info(f"Scraping {username}...")
        self.task.set_status("running_1")
        result = self.scraper.tweets(username)
        if result:
            tweets = [ tweet['text'] for tweet in result["tweets"]]
            if len(tweets) == 0:
                self.task.set_status("failed")
                self.task.data["message"] = "No tweets found"
                return False
            self.task.data["user"] = username
            self.task.data["tweets"] = tweets
            return tweets
        return False

    def analyze(self):
        if not self.task.data["tweets"]:
            return False
        logger.info(f"Analyzing tweets...")
        self.task.set_status("running_2")
        tweets = self.task.data["tweets"]
        try:
            result = self.analyzer.analyze(tweets)
            self.task.data["analysis"] = result[0]
            return result
        except Exception as e:
            self.task.set_status("failed")
            self.task.data["message"] = "Failed to analyze tweets"
            return False

    def result(self):
        if not self.task.data["analysis"]:
            return False
        self.task.set_status("running_3")
        potential_suicidal_tweets = [
            tweet_id for tweet_id, _ in enumerate(self.task.data["tweets"]) if self.task.data["analysis"][tweet_id] == 1
        ]
        pst = len(potential_suicidal_tweets)
        total = len(self.task.data["tweets"])
        suicidal = pst > 0
        message = f"We have found {pst} potential suicidal tweets. We recommend getting this person help." if suicidal else "No potential suicidal tweets found."
        self.task.data["result"] = {
            "suicidal": suicidal,
            "total_tweets": total,
            "ps_tweets": potential_suicidal_tweets,
            "ps_count": pst,
            "message": message,
        }
        self.task.set_status("success")

