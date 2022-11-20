from typing import Dict, List, Optional, Any
from pymongo.operations import UpdateOne
from pymongo import collection
from bson import ObjectId
from ..custom_mongodb_encoders import codec_options
from . import db, _customers


class CustomerDatabase:
    @classmethod
    def _get_coll(cls) -> collection.Collection:
        """
        Returns the relevant collection with pointing to a codec opetion

        Returns:
            collection.Collection: Jobs collection
        """
        return db[_customers].with_options(codec_options=codec_options)

    @classmethod
    def get_customer_by_id(cls, id: str) -> Optional[Any]:
        customer = cls._get_coll().find_one({"_id": ObjectId(id)})
        return customer

    @classmethod
    def get_customer_by_email(cls, email: str) -> Optional[Any]:
        customer = cls._get_coll().find_one({"email": email})
        return customer

    @classmethod
    def add_customer(cls, customer: Dict[str, Any]) -> Optional[bool]:
        # TODO prevent mongodb to create an ID for a new customer
        result = cls._get_coll().insert_one(customer)
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
                        CustomerDatabase._build_array_update_write(field, op, data),
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
    def update_customer(cls, email: str, fields: Dict[str, Any]) -> Optional[bool]:
        writes = cls._adapt_for_bulkwrite(fields, _filter={"email": email})
        result = cls._get_coll().bulk_write(writes)
        return result.acknowledged

    @classmethod
    def delete_customer(cls, customer_email: str) -> Optional[bool]:
        result = cls._get_coll().delete_one({"email": customer_email})
        return result.acknowledged
