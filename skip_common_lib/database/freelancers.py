from typing import Any
from pymongo import command_cursor
from pymongo import collection, results
from pymongo.operations import UpdateOne
from bson import ObjectId

from ..schemas import freelancer as freelancer_schema
from ..schemas import job as job_schema
from ..utils.custom_encoders import codec_options
from . import db, _freelancers


class FreelancerDB:

    location_indexed = False

    @classmethod
    def _get_coll(cls) -> collection.Collection:
        """
        Returns the relevant collection with pointing to a codec opetion.

        Returns:
            collection.Collection: Freelancers collection.
        """
        if not cls.location_indexed:
            db[_freelancers].create_index([("location", "2dsphere")])
            cls.location_indexed = True

        return db[_freelancers].with_options(codec_options=codec_options)

    @classmethod
    async def find_nearest_freelancers(cls, job: job_schema.Job) -> command_cursor.CommandCursor:
        """Finds and returns a list ordered by distance of optional
        freelancers the incoming job.

        Args:
            job (job_model.Job): Incoming job.

        Returns:
            command_cursor.CommandCursor: Cursor of optional freelancers.
        """
        freelancers = await cls._get_coll().aggregate(
            [
                {
                    "$geoNear": {
                        "near": {
                            "type": "Point",
                            "coordinates": [job.job_location[0], job.job_location[1]],
                        },
                        "spherical": True,
                        "query": {
                            "current_status": freelancer_schema.FreelancerStatusEnum.AVAILABLE.value,
                            "county": job.customer_county,
                            "categories": {"$in": [job.job_category]},
                        },
                        "distanceField": "distance",
                    }
                }
            ]
        )
        return freelancers

    @classmethod
    async def get_freelancer_by_id(cls, id: str) -> Any:
        freelancer = await cls._get_coll().find_one({"_id": ObjectId(id)})
        return freelancer

    @classmethod
    async def get_freelancer_by_email(cls, email: str) -> Any:
        freelancer = await cls._get_coll().find_one({"email": email})
        return freelancer

    @classmethod
    async def add_freelancer(
        cls, freelancer: freelancer_schema.Freelancer
    ) -> results.InsertOneResult:
        result = await cls._get_coll().insert_one(freelancer.dict())
        return result

    @classmethod
    async def update_freelancer(
        cls, email: str, freelancer: freelancer_schema.FreelancerUpdate
    ) -> results.UpdateResult:
        result = await cls._get_coll().update_one(
            {"email": email},
            {"$set": freelancer.dict(exclude_none=True)},
        )
        return result

    @classmethod
    async def delete_freelancer(cls, email: str) -> results.DeleteResult:
        result = await cls._get_coll().delete_one({"email": email})
        return result
