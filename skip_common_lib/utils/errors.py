from typing import Any, Dict, Tuple
from flask import jsonify


class Errors:
    @classmethod
    def validation_error(
        cls, exc: Exception, to_validate: Dict[str, Any] = "N/A"
    ) -> Tuple[Dict[str, Any], int]:
        return jsonify(to_validate=to_validate, error_msg=str(exc)), 400

    @classmethod
    def login_failed(cls):
        return jsonify(err_msg="failed to login, probably because invalid email or password")

    @classmethod
    def already_exist_customer_with_email(cls, email: str) -> Tuple[Dict[str, Any], int]:
        return jsonify(err_msg=f"already exist customer with mail: {email}"), 400

    @classmethod
    def already_exist_freelancer_with_email(cls, email: str) -> Tuple[Dict[str, Any], int]:
        return jsonify(err_msg=f"already exist freelancer with mail: {email}"), 400

    @classmethod
    def already_exist_job_with_id(cls, id: str) -> Tuple[Dict[str, Any], int]:
        return jsonify(err_msg=f"already exist content with id: {id}"), 400

    @classmethod
    def general_exception(cls, exc: Exception) -> Tuple[Dict[str, Any], int]:
        return jsonify(err_msg=str(exc)), 400

    @classmethod
    def db_op_not_acknowledged(cls, obj: Any, op: str) -> Tuple[Dict[str, Any], int]:
        return (
            jsonify(err_msg=f"db operation {op.upper()} on {obj} doesn't acknowledged"),
            400,
        )

    @classmethod
    def id_not_found(cls, id: str) -> Tuple[Dict[str, Any], int]:
        return jsonify(err_msg=f"{id} not found"), 404

    @classmethod
    def email_not_found(cls, email: str) -> Tuple[Dict[str, Any], int]:
        return jsonify(err_msg=f"{email} not found"), 404