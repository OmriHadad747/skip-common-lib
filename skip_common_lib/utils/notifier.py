import pydantic as pyd

from typing import List
from pymongo import command_cursor
from firebase_admin import messaging
from flask import current_app as app

from ..models import job as job_model
from ..models import customer as customer_model
from ..models import freelancer as freelancer_model


class Notifier:
    @staticmethod
    def _exclude_failed_tokens(tokens: List[str], resps: List[messaging.SendResponse]) -> List[str]:
        """Finds the failed registration tokens in 'resps' and remove
        them from database cause they are proably invalid.

        Args:
            tokens (List[str]): Registration tokens that a notification pushed to.
            resps (List[messaging.SendResponse]): List of responses from each notification for each freelancer notified.

        Returns:
            List[str]: List of all the registration tokens that actually notified
        """
        failed_tokens = [tokens[idx] for idx, resp in enumerate(resps) if not resp.success]
        app.logger.debug(f"discarding invalid registration tokens {failed_tokens}")

        # TODO implement the call to the db function that remove the registration token from freelancers
        # implement here during testing with real registration tokens

        return [t for t in failed_tokens if t not in tokens]

    @classmethod
    @pyd.validate_arguments
    def push_incoming_job(
        cls, job: job_model.Job, freelancers: command_cursor.CommandCursor
    ) -> List[str]:
        """Found the registration token for each freelancer, and eventually
        trying to push notification for all of them.

        If there are failures with some registation tokens, deleting them frm
        database.

        Args:
            job (job_model.Job): A job to notify freelancers about.
            freelancers (command_cursor.CommandCursor): Cursor of available freelancers

        Returns:
            List[str]: List of all the registration tokens that actually notified
        """
        app.logger.info("notifying freelancers about incoming job")

        tokens = [f.get("registration_token") for f in freelancers]

        msg = messaging.MulticastMessage(data=job.job_to_str(), tokens=tokens)
        resp: messaging.BatchResponse = messaging.send_multicast(msg, dry_run=True)
        # TODO unfreeze here when working with real registration tokens
        # if resp.failure_count > 0:
        #     return cls._exclude_failed_tokens(tokens, resp.responses)

        app.logger.debug(
            f"from {tokens} | {resp.success_count} notified | {resp.failure_count} not notified"
        )
        return tokens

    @classmethod
    @pyd.validate_arguments
    def push_freelancer_found(cls, job: job_model.Job, customer: customer_model.Customer) -> None:
        """Notify a customer that a freelancer has been found for his job

        Args:
            job (job_model.Job): Customer's job.
            customer (customer_model.Customer): Customer to notify.
        """
        app.logger.info("notifying customer that a freelancer was found")

        msg = messaging.Message(
            data=job.job_to_str(freelancer_part=True), token=customer.registration_token
        )
        # resp = messaging.send(msg, dry_run=True)
        resp = None
        app.logger.debug(f"customer notified with message {resp}")

    @classmethod
    @pyd.validate_arguments
    def push_job_quotation(
        cls, quotation: job_model.JobQuotation, customer: customer_model.Customer
    ) -> None:
        # TODO write docstring
        app.logger.info("notifying customer about job quotation")

        msg = messaging.Message(
            data=quotation.quotation_to_str(), token=customer.registration_token
        )
        # resp = messaging.send(msg, dry_run=True)

        # app.logger.debug(f"customer notified with message {resp}")

    @classmethod
    @pyd.validate_arguments
    def push_quotation_confirmation(
        cls,
        job_id: str,
        freelancer: freelancer_model.Freelancer,
        job_status: job_model.JobStatusEnum,
    ) -> None:
        # TODO write docstring
        app.logger.info(
            f"notifying freelancer {freelancer.email} about job quotation approved/canceld for job {job_id}"
        )

        msg = messaging.MulticastMessage(
            data={"message": f"job {job_id} approved"},
            tokens=freelancer.registration_token,
        )
        resp: messaging.BatchResponse = messaging.send_multicast(msg, dry_run=True)
        # TODO unfreeze here when working with real registration tokens
        # if resp.failure_count > 0:
        #     return cls._exclude_failed_tokens(
        #         [customer.registration_token, freelancer.registration_token], resp.responses
        #     )

        app.logger.debug(f"customer and freelancer are both notified")
