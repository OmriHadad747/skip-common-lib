import json
import bson
import datetime

from datetime import datetime, date
from flask import current_app
from flask_pymongo import ObjectId
from ..models.job import JobCategoryEnum, JobStatusEnum


# TODO understand where I use this and how
class CustomeEncoder(json.JSONEncoder):
    # TODO write docstring for this class
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return str(obj)

        return super(CustomeEncoder, self).default(obj)


current_app.json_encoder = CustomeEncoder


def custom_serializer(obj):
    """
    JSON serializer for objects not serializable by default
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, (JobStatusEnum, JobCategoryEnum)):
        return obj.value
    elif isinstance(obj, ObjectId):
        return str(obj)
