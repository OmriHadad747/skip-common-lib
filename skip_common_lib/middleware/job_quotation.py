import pydantic as pyd

from functools import wraps
from typing import Any, Callable

from ..utils.errors import Errors as err
from ..schemas import job as job_schema
from ..database.jobs import JobDB as db


def update_job_quotation(quote_func: Callable[[Any], dict[str, Any] | None]):
    """
    Validate given quotation fields and updates the incoming job in database.

    Args:
        quote_func (Callable[[Any], dict[str, Any] | None])
    """

    @wraps(quote_func)
    async def update_job_quotation_wrapper(*args):
        _cls = args[0]
        job_id: str = args[1]
        quotation: job_schema.JobQuotation = args[2]

        try:
            job = job_schema.JobUpdate(
                **{
                    "job_quotation": quotation,
                }
            )

            #  app.logger.debug(f"updating job {job_id} in db with quotation data")

            res = await db.update_job(
                job_id, job, curr_job_status=job_schema.JobStatusEnum.FREELANCER_FOUND
            )
            if not res.acknowledged:
                return err.db_op_not_acknowledged(job.dict(exclude_none=True), op="update")

            #  app.logger.debug(f"job {job_id} updated in db")

        except pyd.ValidationError as e:
            return err.validation_error(e)
        except Exception as e:
            return err.general_exception(e)

        return await quote_func(_cls, job_id, quotation)

    return update_job_quotation_wrapper


def update_job_approved_or_declined(approved_func: Callable[[Any], dict[str, Any] | None]):
    """Updating a job that it is approved.

    Args:
        approved_func (Callable[[Any], dict[str, Any] | None])
    """

    @wraps(approved_func)
    async def update_job_approved_or_declined_wrapper(*args):
        _cls = args[0]
        job_id: str = args[1]
        approved: bool = args[2]

        if not isinstance(bool, approved):
            raise pyd.ValidationError("approved flag is not a boolean")

        try:
            job = job_schema.JobUpdate(
                **{
                    "job_status": job_schema.JobStatusEnum.APPROVED
                    if approved
                    else job_schema.JobStatusEnum.CUSTOMER_CANCELD
                }
            )

            res = await db.update_job(
                job_id, job, curr_job_status=job_schema.JobStatusEnum.FREELANCER_FOUND
            )
            if not res.acknowledged:
                return err.db_op_not_acknowledged(job.dict(exclude_none=True), op="update")

        except pyd.ValidationError as e:
            return err.validation_error(e)
        except Exception as e:
            return err.general_exception(e)

        return await approved_func(_cls, job_id)

    return update_job_approved_or_declined_wrapper
