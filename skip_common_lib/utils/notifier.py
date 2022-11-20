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


def _nofity_freelancers(
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


    def _notify_customer(cls, job: job_model.Job, customer: customer_model.Customer) -> None:
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