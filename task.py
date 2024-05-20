import json
import uuid

import uuid
import json
from sqlalchemy import create_engine, Column, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import JSON


TASK_STATUS_MAP = json.loads(open("task_status.json").read())


# Define the SQLAlchemy base and session
Base = declarative_base()
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)

def update_task(id, **kwargs):
    with Session() as session:
        task = session.query(Task).filter_by(id=id).first()
        for key, value in kwargs.items():
            if hasattr(task, key):
                if key == "status":
                    value = TASK_STATUS_MAP.get(value, TASK_STATUS_MAP["created"])
                setattr(task, key, value)
        session.commit()

def get_task_json(id):
    result = {}
    with Session() as session:
        task = session.query(Task).filter_by(id=id).first()
        for key, value in task.as_dict().items():
            if hasattr(task, key):
                result[key] = getattr(task, key)
    return result
class Task(Base):
    __tablename__ = 'tasks2'

    id = Column(String, primary_key=True)
    status = Column(JSON, nullable=True, default=TASK_STATUS_MAP["created"])
    username = Column(String, nullable=True)
    tweets = Column(JSON, nullable=True)
    analysis = Column(JSON, nullable=True)
    message = Column(Text, nullable=True)
    suicidal = Column(Boolean, nullable=True)
    ps_tweets = Column(JSON, nullable=True)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


    def __init__(self, username=None, tweets=None, analysis=None, message=None, suicidal=None, ps_tweets=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.tweets = tweets
        self.analysis = analysis
        self.message = message
        self.suicidal = suicidal
        self.ps_tweets = ps_tweets

    def save(self):
        session = Session()
        session.add(self)
        session.commit()
        session.close()




    # result = Column(, nullable=True)

    # def __init__(self, status=None, data=None):
    #     self.status = status or TASK_STATUS_MAP["created"]
    #     self.data = data or {
    #         "user": None,
    #         "tweets": None,
    #         "analysis": None,
    #         "message": None,
    #         "result": None,
    #     }
    # # update the task data while avoiding detached instance error
    # def update(self, data):
    #     session = Session()
    #     task = session.query(Task).filter_by(id=self.id).first()
    #     task.data = data
    #     session.commit()
    #     session.close()


    # def set_status(self, status_str):
    #     self.status = TASK_STATUS_MAP.get(status_str, TASK_STATUS_MAP["created"])

    # def serialize(self):
    #     return json.dumps({
    #         "id": self.id,
    #         "status": self.status,
    #         "data": self.data,
    #     })

    # def deserialize(self, json_str):
    #     data = json.loads(json_str)
    #     self.id = data["id"]
    #     self.status = data["status"]
    #     self.data = data["data"]

    # def save_to_db(self):
    #     session = Session()
    #     session.add(self)
    #     session.commit()
    #     session.close()

    # @staticmethod
    # def get_from_db(task_id):
    #     session = Session()
    #     task = session.query(Task).filter_by(id=task_id).first()
    #     session.close()
    #     return task

# Create the table in the database
Base.metadata.create_all(engine)


# class Task:
#     def __init__(self, status=None, data=None):
#         self.id = uuid.uuid4()
#         self.status = status or TASK_STATUS_MAP["created"]
#         self.data = data or {
#             "user": None,
#             "tweets": None,
#             "analysis": None,
#             "message": None,
#             "result": None,
#         }
#     def set_status(self, status_str):
#         self.status = TASK_STATUS_MAP.get(status_str, TASK_STATUS_MAP["created"])

#     def serialize(self):
#         return json.dumps({
#             "id": self.id,
#             "status": self.status,
#             "data": self.data,
#         })

#     def deserialize(self, json_str):
#         data = json.loads(json_str)
#         self.id = data["id"]
#         self.status = data["status"]
#         self.data = data["data"]

