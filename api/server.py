# from queue import TaskQueue, QueueConnection
from api.queue import TaskQueue, QueueConnection
import fastapi
import logging
from task import Task

app = fastapi.FastAPI()
queue = TaskQueue(QueueConnection(), "tasks")
logger = logging.getLogger()

@app.get("/task")
def get_task(username : str):
    task = Task()
    task.data["user"] = username
    json_task = task.serialize()
    queue.send(json_task)
