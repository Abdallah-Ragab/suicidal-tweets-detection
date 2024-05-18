import os
import pika


HOST = os.getenv('RABBITMQ_HOST') or 'localhost'

class QueueConnection:
    def __init__(self, host=HOST):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def close(self):
        self.connection.close()

class Worker:
    def __init__(self):
        self.connection = QueueConnection()
        self.queue = TaskQueue(self.connection, 'scraper', self.callback)