from logging import Logger

from typing import Any
from fastapi import status, HTTPException


class Errors:
    @classmethod
    def validation_error(cls, exc: Exception):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @classmethod
    def login_failed(cls):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="failed to login, probably because invalid email or password",
        )

    @classmethod
    def already_exist_customer_with_email(cls, email: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"already exist customer with mail: {email}",
        )

    @classmethod
    def already_exist_freelancer_with_email(cls, email: str, logger: Logger = None):
        if logger:
            logger.debug(f"already exist freelancer with mail: {email}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"already exist freelancer with mail: {email}",
        )

    @classmethod
    def already_exist_job_with_id(cls, id: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"already exist job with id: {id}"
        )

    @classmethod
    def general_exception(cls, exc: Exception):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    @classmethod
    def db_op_not_acknowledged(cls, obj: Any, op: str, logger: Logger = None):
        if logger:
            logger.error(f"db operation {op.upper()} on {obj} doesn't acknowledged")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"db operation {op.upper()} on {obj} doesn't acknowledged",
        )

    @classmethod
    def id_not_found(cls, id: str, logger: Logger = None):
        if logger:
            logger.error(f"{id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")

    @classmethod
    def email_not_found(cls, email: str, logger: Logger = None):
        if logger:
            logger.error(f"{email} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{email} not found")
