from typing import Any
from bson import ObjectId
from pymongo import collection, results

from ..schemas import job as job_schema
from ..utils.custom_encoders import codec_options
from . import db, _jobs


class JobDB:
    @classmethod
    def _get_coll(cls) -> collection.Collection:
        """
        Returns the relevant collection with pointing to a codec opetion.

        Returns:
            collection.Collection: Jobs collection.
        """
        return db[_jobs].with_options(codec_options=codec_options)

    @classmethod
    async def get_job_by_id(cls, id: str) -> dict[str, Any]:
        job = await cls._get_coll().find_one({"_id": ObjectId(id)})
        return job

    @classmethod
    async def add_job(cls, job: job_schema.Job) -> results.InsertOneResult:
        result = await cls._get_coll().insert_one(job.dict(by_alias=True))
        return result

    @classmethod
    async def update_job(
        cls, id: str, job: job_schema.JobUpdate, curr_job_status: job_schema.JobStatusEnum
    ) -> results.UpdateResult:
        result = await cls._get_coll().update_one(
            {"_id": ObjectId(id), "job_status": curr_job_status.value},
            {"$set": job.dict(exclude_none=True)},
        )
        return result
