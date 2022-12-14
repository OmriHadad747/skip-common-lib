import json
import bson
import datetime

from datetime import datetime, date
from flask import current_app
from flask_pymongo import ObjectId
from bson.codec_options import TypeEncoder, TypeRegistry, CodecOptions
from ..models.job import JobCategoryEnum, JobStatusEnum
from ..models.freelancer import FreelancerStatusEnum


class JobCategoryEncoder(TypeEncoder):

    python_type = JobCategoryEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


class JobStatusEncoder(TypeEncoder):

    python_type = JobStatusEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


class FreelancertatusEncoder(TypeEncoder):

    python_type = FreelancerStatusEnum  # the Python type acted upon by this type codec

    def transform_python(self, value):
        """
        Function that transforms a custom type value into a type
        that BSON can encode.
        """
        return value.value


# TODO understand where I use this and how
class CustomeEncoder(json.JSONEncoder):
    # TODO write docstring for this class
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return str(obj)

        return super(CustomeEncoder, self).default(obj)


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


current_app.json_encoder = CustomeEncoder

job_category_encoder = JobCategoryEncoder()
job_status_encoder = JobStatusEncoder()
freelancer_status_encoder = FreelancertatusEncoder()
type_registry = TypeRegistry([job_category_encoder, job_status_encoder, freelancer_status_encoder])
codec_options = CodecOptions(type_registry=type_registry)
