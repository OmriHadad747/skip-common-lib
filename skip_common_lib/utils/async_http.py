import enum
import httpx
import tenacity
import logging

from typing import Any

from ..consts import HttpMethod


class RetryIfNotStatus(tenacity.retry_if_exception):
    """Retries only if a response status code is NOT of the following."""

    def __init__(self, status_codes: list[int] | None = None) -> None:
        if status_codes is None:
            # TODO re-think what statuses will trigger a retry
            status_codes = [
                401,
                402,
                404,
                405,
                406,
            ]

        super().__init__(
            lambda e: e.response.status_code not in status_codes
            if isinstance(e, httpx.HTTPStatusError)
            else False
        )


class AsyncHttp:

    logger = logging.getLogger()

    @classmethod
    def _log_retry_attempt(cls, retry_state: tenacity.RetryCallState) -> None:
        """Logs which URL is being retried.

        Args:
            retry_state (tenacity.RetryCallState)
        """
        if url := retry_state.kwargs.get("url"):
            cls.logger.info(f"retrying request to {url}")
        elif retry_state.args:
            cls.logger.info(f"retrying request to {retry_state.args[0]}")

    @classmethod
    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=30, min=2, max=4),
        stop=tenacity.stop_after_attempt(4),
        retry=RetryIfNotStatus(),
        before=_log_retry_attempt,
        reraise=True,
    )
    async def http_call(cls, **kwargs) -> httpx.Response:
        """Single entry point for making an http request.

        Raises:
            ValueError: In case the provided http method is undefined.

        Returns:
            httpx.Response: The response of the executed http request.
        """
        http_method: HttpMethod = kwargs.pop("method", HttpMethod.GET)
        if not HttpMethod.valid_method(http_method.value):
            cls.logger.error(f"invalid httpd method provided: {http_method}")
            raise ValueError(f"invalid method: {http_method}")

        resp: httpx.Response = await eval(f"cls._{http_method.value}(**{kwargs})")

        cls.logger.info(
            f"response info from endpoint: {resp.request.url} || status code: {resp.status_code} || response: {resp.json() or 'None'}"
        )

        resp.raise_for_status()
        return resp

    @classmethod
    async def _get(cls, **kwargs: dict[str, Any]) -> httpx.Response:
        url, headers, auth, params = (
            kwargs.pop("url", None),
            kwargs.pop("headers", {}),
            kwargs.pop("auth", None),
            kwargs.pop("params", {}),
        )

        cls.logger.info(f"Sending GET request to: {url}")

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url=url, headers=headers, auth=auth, params=params)

        return resp

    @classmethod
    async def _post(cls, **kwargs: dict[str, Any]) -> httpx.Response:
        url, headers, auth, params, json = (
            kwargs.pop("url", None),
            kwargs.pop("headers", {}),
            kwargs.pop("auth", None),
            kwargs.pop("params", {}),
            kwargs.pop("json", {}),
        )

        cls.logger.info(f"Sending POST request to: {url}\nPayload: {json or 'None'}")

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(url=url, headers=headers, auth=auth, params=params, json=json)

        return resp

    @classmethod
    async def _put(cls, **kwargs: dict[str, Any]) -> httpx.Response:
        url, headers, auth, params, json = (
            kwargs.pop("url", None),
            kwargs.pop("headers", {}),
            kwargs.pop("auth", None),
            kwargs.pop("params", {}),
            kwargs.pop("json", {}),
        )

        cls.logger.info(f"Sending PUT request to {url}\nPayload: {json or 'None'}")

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.put(
                url=url,
                headers=headers,
                auth=auth,
                params=params,
                json=json,
            )

        return resp

    @classmethod
    async def _patch(cls, **kwargs: Any) -> httpx.Response:
        url, headers, auth, params, json = (
            kwargs.pop("url", None),
            kwargs.pop("headers", {}),
            kwargs.pop("auth", None),
            kwargs.pop("params", {}),
            kwargs.pop("json", {}),
        )

        cls.logger.info(f"Sending PATCH request to {url}\nPayload: {json or 'None'}")

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.patch(
                url=url,
                headers=headers,
                auth=auth,
                params=params,
                json=json,
            )

        return resp

    @classmethod
    async def _delete(cls, **kwargs: Any) -> httpx.Response:
        url, headers, auth, params, json = (
            kwargs.pop("url", None),
            kwargs.pop("headers", {}),
            kwargs.pop("auth", None),
            kwargs.pop("params", {}),
            kwargs.pop("json", {}),
        )

        cls.logger.info(f"Sending DELETE request to {url}")

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.delete(
                url=url,
                headers=headers,
                auth=auth,
                params=params,
                json=json,
            )

        return resp
