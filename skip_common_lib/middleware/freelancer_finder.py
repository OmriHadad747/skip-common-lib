import pydantic as pyd

from functools import wraps
from typing import Any, Callable

from ..utils.errors import Errors as err
from ..schemas import job as job_schema
from ..schemas import freelancer as freelancer_schema
from ..database.jobs import JobDB as db


def save_incoming_job(find_func: Callable[[Any], dict[str, Any] | None]):
    """
    Validates and save the incoming job to database.
    Eventually, pushing forwared to the decorated function a validate job model.

    Args:
        find_func (Callable[[Any], dict[str, Any] | None]): Decorated function
    """

    @wraps(find_func)
    async def save_incoming_job_wrapper(*args):
        _cls = args[0]
        incoming_job: job_schema.Job = args[1]

        try:
            #  app.logger.debug(f"saving to database the following job {incoming_job.dict()}")

            res = await db.add_job(incoming_job)
            if not res.acknowledged:
                return err.db_op_not_acknowledged(incoming_job.dict(), op="insert")

            #  app.logger.debug(f"job {res.inserted_id} saved to database")

        except pyd.ValidationError as e:
            return err.validation_error(e)
        except Exception as e:
            return err.general_exception(e)

        return await find_func(_cls, incoming_job)

    return save_incoming_job_wrapper


def update_incoming_job(take_func: Callable[[Any], dict[str, Any] | None]):
    """
    Validate given freelancer fields and updates the incoming job in database.

    Args:
        take_func (Callable[[Any], dict[str, Any] | None]): Decorated function.
    """

    @wraps(take_func)
    async def update_incoming_job_wrapper(*args):
        _cls = args[0]
        job_id: str = args[1]
        freelancer: freelancer_schema.FreelancerTakeJob = args[2]

        try:
            job = job_schema.JobUpdate(
                **{
                    "freelancer_email": freelancer.freelancer_email,
                    "freelancer_phone": freelancer.freelancer_phone,
                    "job_status": job_schema.JobStatusEnum.FREELANCER_FOUND,
                }
            )

            #  app.logger.debug(f"updating job {job_id} in database with freelancer data")

            res = await db.update_job(
                job_id, job, curr_job_status=job_schema.JobStatusEnum.FREELANCER_FINDING
            )
            if res.matched_count == 0 and res.modified_count == 0:
                #  app.logger.debug(f"job {job_id} was already taken by another freelancer")
                return take_func(_cls)

            if not res.acknowledged:
                return err.db_op_not_acknowledged(job.dict(exclude_none=True), op="update")

            #  app.logger.debug(f"job {job_id} updated in database")

        except pyd.ValidationError as e:
            return err.validation_error(e)
        except Exception as e:
            return err.general_exception(e)

        return await take_func(_cls, job_id)

    return update_incoming_job_wrapper
