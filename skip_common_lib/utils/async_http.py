import httpx

from logging import Logger
from typing import Any

from ..consts import HttpMethod


class AsyncHttp:
    @classmethod
    async def http_call(cls, logger: Logger | None = None, **kwargs) -> httpx.Response:
        """Single entry point for making an http request.

        Args:
            logger (Logger | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: In case the provided http method is undefined.

        Returns:
            httpx.Response: The response of the executed http request.
        """
        http_method: HttpMethod = kwargs.pop("method", HttpMethod.GET)
        if not HttpMethod.valid_method(http_method.value):
            if logger:
                logger.error(f"invalid httpd method provided: {http_method}")
            raise ValueError(f"invalid method: {http_method}")

        if logger:
            logger.info(
                f"sending {http_method.value.upper()} request to {kwargs.get('url')} || payload : {kwargs.get('json') or None}"
            )

        resp: httpx.Response = await eval(f"cls._{http_method.value}(**{kwargs})")

        if logger:
            logger.info(
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

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.delete(
                url=url,
                headers=headers,
                auth=auth,
                params=params,
                json=json,
            )

        return resp
