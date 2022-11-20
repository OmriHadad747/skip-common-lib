from typing import Dict, List, Optional, Any
from pymongo import command_cursor
from pymongo import collection
from pymongo.operations import UpdateOne
from bson import ObjectId
from ..models import freelancer as freelancer_model
from ..models import job as job_model
from ..custom_mongodb_encoders import codec_options
from . import db, _freelancers


class FreelancerDatabase:

    location_indexed = False

    @classmethod
    def _get_coll(cls) -> collection.Collection:
        """
        Returns the relevant collection with pointing to a codec opetion

        Returns:
            collection.Collection: Jobs collection
        """
        if not cls.location_indexed:
            db[_freelancers].create_index([("location", "2dsphere")])
            cls.location_indexed = True

        return db[_freelancers].with_options(codec_options=codec_options)

    @classmethod
    def find_nearest_freelancers(cls, job: job_model.Job) -> command_cursor.CommandCursor:
        # TODO write docstring
        freelancers = cls._get_coll().aggregate(
            [
                {
                    "$geoNear": {
                        "near": {
                            "type": "Point",
                            "coordinates": [job.job_location[0], job.job_location[1]],
                        },
                        "spherical": True,
                        "query": {
                            "current_status": freelancer_model.FreelancerStatusEnum.AVAILABLE.value,
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
    def get_freelancer_by_id(cls, id: str) -> Optional[Any]:
        freelancer = cls._get_coll().find_one({"_id": ObjectId(id)})
        return freelancer

    @classmethod
    def get_freelancer_by_email(cls, email: str) -> Optional[Any]:
        freelancer = cls._get_coll().find_one({"email": email})
        return freelancer

    @classmethod
    def add_freelancer(cls, freelancer: Dict[str, Any]) -> Optional[bool]:
        result = cls._get_coll().insert_one(freelancer)
        return result.acknowledged

    @staticmethod
    def _build_array_update_write(field: str, op: str, data: List[Any]) -> Optional[Dict[str, Any]]:
        """
        - building 'update' argument for PyMongo's UpdateOne method
        for document fields that are an array type

        Args:
            - field (str): document's field name to update
            - op (str): operation to perform. available options: ['add', 'rem']
            - data (List[Any]): data to add or remove from the document's field

        Raises:
            - ValueError: in case of unknown/unsupported 'op' (operation)

        Returns:
            - Optional[Dict[str, Any]]: dictionary that can be rendered by MongoDB driver
        """
        if op == "add":
            return {"$addToSet": {field: {"$each": data}}}
        elif op == "rem":
            return {"$pull": {field: {"$in": data}}}
        else:
            raise ValueError(f"unknown operation - {op}")

    @staticmethod
    def _adapt_for_bulkwrite(
        fields_to_update: Dict[str, Any], _filter: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        """
        - iterate through all the provided document fields and build a list of updates
        to perform using the 'bulk_write' method

        - in case a field is an array type, use '_build_array_update_write' static function
        to create an 'update' object appropriate for an array

        Args:
            - fields_to_update (Dict[str, Any]): bunch of fields to update in a document
            - _filter (Dict[str, Any]): filter to apply on the updates

        Raises:
            - ValueError:
                - in case an array field doesn't have kind of operation ['add', 'rem'] to perform
                - in case an array field contains more then 1 operation ['add', 'rem'] to perform

        Returns:
            - Optional[List[Dict[str, Any]]]: list of updateOne operation to perform as part of the 'bulk_write' method
        """
        writes = []

        basic_update_write = {"$set": {}}

        for field, val in fields_to_update.items():
            if isinstance(val, dict):
                if len(val) == 0 or len(val) > 1:
                    raise ValueError(
                        f"'{field}' can't be empty or contain more then 1 key/operation ['add', 'rem']"
                    )

                op, data = val.popitem()
                writes.append(
                    UpdateOne(
                        _filter,
                        FreelancerDatabase._build_array_update_write(field, op, data),
                    )
                )
            else:
                basic_update_write["$set"][field] = val

        # append the '$set' update operation at the end of the list so it will be
        # executed last, such that in case the user's email is a part of the
        # update, filtering by user's email will not work (cause the user's email changed)
        if len(basic_update_write.get("$set")) > 0:
            writes.append(UpdateOne(_filter, basic_update_write))

        return writes

    @classmethod
    def update_freelancer(cls, email: str, fields: Dict[str, Any]) -> Optional[bool]:
        writes = cls._adapt_for_bulkwrite(fields, _filter={"email": email})
        result = cls._get_coll().bulk_write(writes)
        return result.acknowledged

    @classmethod
    def delete_freelancer(cls, email: str) -> Optional[bool]:
        result = cls._get_coll().delete_one({"email": email})
        return result.acknowledged
