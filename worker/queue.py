import os
import pika


HOST = os.getenv('RABBITMQ_HOST') or 'localhost'

class QueueConnection:
    def __init__(self, host=HOST):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def close(self):
        self.connection.close()

class TaskQueue:
    def __init__(self, connection, queue_name, callback=None):
        self.name = queue_name
        self.connection = connection
        self.channel = self.connection.channel
        self.channel.queue_declare(queue=queue_name, durable=True)
        if callback:
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback)

    def listen(self):
        self.channel.start_consuming()