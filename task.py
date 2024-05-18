import json
import uuid


TASK_STATUS_MAP = json.loads(open("task_status.json").read())


class Task:
    def __init__(self, status=None, data=None):
        self.id = uuid.uuid4()
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

