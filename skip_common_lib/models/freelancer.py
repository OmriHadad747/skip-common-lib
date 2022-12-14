import pydantic as pyd

from typing import List
from datetime import datetime
from enum import Enum
from flask_pymongo import ObjectId
from ..models import job as job_model
from ..models import CustomBaseModel


class FreelancerCategoryEnum(Enum):
    GARAGE = 0
    LOCKSMITH = 1
    MOVING = 2


class FreelancerStatusEnum(Enum):
    AVAILABLE = 0
    BUSY = 1


class Freelancer(CustomBaseModel):
    created_at: datetime = pyd.Field(default_factory=datetime.now)
    _id: int = ObjectId()
    password: str
    email: str
    phone: str
    county: str
    tmp_county: str = None
    tmp_county_date: datetime = None
    categories: pyd.conlist(item_type=FreelancerCategoryEnum)
    current_status: FreelancerStatusEnum = FreelancerStatusEnum.AVAILABLE.value
    rating: float = 1.0
    job_history: List[job_model.Job] = []
    location: pyd.conlist(item_type=float, min_items=2, max_items=2)
    location_date: datetime = pyd.Field(default_factory=datetime.now)
    registration_token: str


class FreelancerUpdate(CustomBaseModel):
    updated_at: datetime = pyd.Field(default_factory=datetime.now)
    password: str = None
    email: str = None
    phone: str = None
    county: str = None
    tmp_county: str = None
    tmp_county_date: datetime = None
    categories: pyd.conlist(item_type=FreelancerCategoryEnum) = None
    current_status: FreelancerStatusEnum = None
    rating: float = None
    current_location: pyd.conlist(item_type=float, min_items=2, max_items=2) = None
    current_location_date: datetime = None
    registration_token: str = None


class FreelancerTakeJob(CustomBaseModel):
    freelancer_email: str
    freelancer_phone: str
