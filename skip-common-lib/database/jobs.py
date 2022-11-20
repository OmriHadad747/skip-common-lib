from typing import Any, Dict
from bson import ObjectId
from pymongo import collection, results
from ..models import job as job_model
from ..custom_mongodb_encoders import codec_options
from . import db, _jobs


class JobDatabase:
    @classmethod
    def _get_coll(cls) -> collection.Collection:
        """
        Returns the relevant collection with pointing to a codec opetion

        Returns:
            collection.Collection: Jobs collection
        """
        return db[_jobs].with_options(codec_options=codec_options)

    @classmethod
    def add_job(cls, job: job_model.Job) -> results.InsertOneResult:
        result = cls._get_coll().insert_one(job.dict(by_alias=True))
        return result

    @classmethod
    def get_job_by_id(cls, id: str) -> Dict[str, Any]:
        job = cls._get_coll().find_one({"_id": ObjectId(id)})
        return job

    @classmethod
    def update_job(
        cls, id: str, job: job_model.JobUpdate, curr_job_status: job_model.JobStatusEnum
    ) -> results.UpdateResult:
        result = cls._get_coll().update_one(
            {"_id": ObjectId(id), "job_status": curr_job_status.value},
            {"$set": job.dict(exclude_none=True)},
        )
        return result
