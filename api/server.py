# from queue import TaskQueue, QueueConnection
from api.queue import TaskQueue, QueueConnection
import fastapi
import logging
from task import Task, update_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware


engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)

app = fastapi.FastAPI()
queue = TaskQueue(QueueConnection(), "tasks")
logger = logging.getLogger()


origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/task")
def get_task(username : str):
    task = Task(username=username)
    task_id = task.id
    task.save()
    queue.send(task_id)
    update_task(task_id, status='waiting')
    return {"task_id": task_id}


@app.get("/check")
def check_task(task_id: str):
    with Session() as session:
        task = session.query(Task).filter_by(id=task_id).first()
        return task.as_dict()