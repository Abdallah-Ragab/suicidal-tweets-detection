import json
import os
import pika
from tqueue import TaskQueue, QueueConnection
from scraper.scraper import Scraper
from analyzer.analyzer import Analyzer
import logging
import sys
sys.path.append("D:\Repositories\suicidal-tweets-detection")
from task import Task, update_task, get_task_json

logger = logging.getLogger()

TASK_QUEUE_NAME = "tasks"

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
        task_id = body.decode()
        self.task_id = task_id
        update_task(self.task_id, status='scheduled')
        logger.info(f"Received task: {task_id}")
        self.do()
        self.done()

    def ready(self):
        self.queue.listen()

    def done(self):
        self.received_task["channel"].basic_ack(delivery_tag=self.received_task["method"].delivery_tag)

    def do(self):
        update_task(self.task_id, status='running_1')
        result = self.scrape()
        if not result:
            logger.error(f"Task {self.task_id} failed. Could not scrape tweets.")
            return False

        update_task(self.task_id, status='running_2')
        result = self.analyze()
        if not result:
            logger.error(f"Task {self.task_id} failed. Could not analyze tweets.")
            return False

        update_task(self.task_id, status='running_3')
        result = self.result()
        if not result:
            logger.error(f"Task {self.task_id} failed. Could not get results.")
            return False

        logger.info(f"Task {self.task_id} completed successfully.")


    def scrape(self):
        username = get_task_json(self.task_id)['username']
        logger.info(f"Scraping {username}...")
        result = self.scraper.tweets(username)
        print(result)
        if result:
            tweets = [ tweet['text'] for tweet in result["tweets"]]
            if len(tweets) == 0:
                update_task(self.task_id, status='failed')
                update_task(self.task_id, message='No tweets found')
                return False
            update_task(self.task_id, tweets={'tweets': tweets})
            return tweets
        return False

    def analyze(self):
        task = get_task_json(self.task_id)

        if not task["tweets"]["tweets"]:
            return False
        logger.info(f"Analyzing tweets...")
        tweets = task["tweets"]["tweets"]
        try:
            result = self.analyzer.analyze(tweets)
            update_task(self.task_id, analysis={'analysis': result[0]})
            return result
        except Exception as e:
            update_task(self.task_id, status='failed')
            update_task(self.task_id, message='Failed to analyze tweets')
            return False

    def result(self):
        task = get_task_json(self.task_id)
        tweets = task['tweets']["tweets"]
        analysis = task['analysis']['analysis']
        if not analysis or not tweets:
            return False
        potential_suicidal_tweets = [
            tweet_id for tweet_id, _ in enumerate(tweets) if analysis[tweet_id] == 1
        ]
        pst = len(potential_suicidal_tweets)
        suicidal = pst > 0
        message = f"We have found {pst} potential suicidal tweets. We recommend getting this person help." if suicidal else "No potential suicidal tweets found."
        update_task(self.task_id, status='success', message=message, suicidal=suicidal, ps_tweets={'tweets': potential_suicidal_tweets})


