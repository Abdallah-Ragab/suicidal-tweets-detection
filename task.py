import json
import uuid

import uuid
import json
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TASK_STATUS_MAP = json.loads(open("task_status.json").read())


# Define the SQLAlchemy base and session
Base = declarative_base()
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, nullable=False)
    data = Column(Text, nullable=False)

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
            "id": self.id,
            "status": self.status,
            "data": self.data,
        })

    def deserialize(self, json_str):
        data = json.loads(json_str)
        self.id = data["id"]
        self.status = data["status"]
        self.data = data["data"]

    def save_to_db(self):
        session = Session()
        session.add(self)
        session.commit()
        session.close()

    @staticmethod
    def get_from_db(task_id):
        session = Session()
        task = session.query(Task).filter_by(id=task_id).first()
        session.close()
        return task

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

