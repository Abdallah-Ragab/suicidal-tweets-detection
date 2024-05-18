# from queue import TaskQueue, QueueConnection
from api.queue import TaskQueue, QueueConnection
import fastapi
import logging

app = fastapi.FastAPI()
queue = TaskQueue(QueueConnection(), "tasks")
logger = logging.getLogger()

@app.get("/task")
def get_task(username : str):
    queue.send(username)
    logger.info(f"Task sent to worker for {username}")
    return {"message": "Task sent to worker"}

