import logging
from typing import Any, Self

import httpx

from jsm._http import create_basic_client, request_json

logger = logging.getLogger("jsm")

OPS_AUTH_HINT = (
    " Check API token has JSM Ops scope read:ops-config:jira-service-management "
    "(classic token from id.atlassian.com, or scoped token with Bearer via use_bearer)."
)


class Schedules:
    """
    Jira Service Management operations (on-call) schedules API.
    Drop-in replacement for opsgenie.Schedules using JSM Ops REST API.
    """

    def __init__(self, auth: dict[str, Any]) -> None:
        cloud_id = auth["cloud_id"]
        self._base_url = f"https://api.atlassian.com/jsm/ops/api/{cloud_id}/v1"
        self._auth = auth
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        self._client = create_basic_client(self._auth, base_url=self._base_url)
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _client_or_raise(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Use 'async with Schedules(...)' before calling API methods")
        return self._client

    async def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> Any:
        client = self._client_or_raise()
        hint = OPS_AUTH_HINT if method == "GET" else ""
        return await request_json(client, method, path, params=params, hint=hint)

    @staticmethod
    def _unwrap_response(resp: Any) -> Any:
        if isinstance(resp, dict) and "data" in resp:
            return resp["data"]
        return resp

    async def _get_paginated_values(self, path: str, params: dict[str, Any] | None = None) -> Any:
        params = dict(params or {})
        size = min(params.pop("size", 50), 50)
        results: list[Any] = []
        offset = 0
        while True:
            resp = self._unwrap_response(
                await self._request("GET", path, params={**params, "offset": offset, "size": size})
            )
            if not isinstance(resp, dict) or "values" not in resp:
                return resp
            batch = resp["values"]
            results.extend(batch)
            if len(batch) < size:
                break
            offset += size
        return results

    async def get(self, path: str, **kwargs: Any) -> Any:
        params = kwargs.get("params")
        return self._unwrap_response(await self._request("GET", path, params=params))

    async def get_schedules(self, identifier: str | None = None) -> Any:
        url = "/schedules"
        if identifier:
            url += f"/{identifier}"
            return await self.get(url)
        return await self._get_paginated_values(url)

    async def get_schedule_timeline(
        self,
        identifier: str,
        identifier_type: str | None = None,
        expand: bool | str | None = None,
        interval: int | None = None,
        interval_unit: str | None = None,
        date: str | None = None,
        *,
        identifierType: str | None = None,  # noqa: N803
        intervalUnit: str | None = None,  # noqa: N803
    ) -> Any:
        identifier_type = identifier_type or identifierType
        interval_unit = interval_unit or intervalUnit
        params: dict[str, Any] = {}
        if identifier_type:
            params["identifierType"] = identifier_type
        if expand is True:
            params["expand"] = "base"
        elif expand:
            params["expand"] = expand
        if interval is not None:
            params["interval"] = interval
        if interval_unit:
            params["intervalUnit"] = interval_unit
        if date:
            params["date"] = date
        return await self.get(f"/schedules/{identifier}/timeline", params=params)

    async def get_schedule_rotations(self, identifier: str) -> Any:
        return await self.get(f"/schedules/{identifier}/rotations")

    async def get_schedule_overrides(self, identifier: str) -> Any:
        return await self.get(f"/schedules/{identifier}/overrides")

    async def get_users(self, identifier: str | None = None) -> Any:
        url = "/users"
        if identifier:
            url += f"/{identifier}"
            user = await self.get(url)
            return self._normalize_user(user)
        try:
            users = await self._get_paginated_values(url)
            return [self._normalize_user(u) for u in users]
        except httpx.HTTPStatusError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                logger.warning(
                    "JSM Ops API: /users endpoint not available (404); "
                    "user display names will fall back to email addresses."
                )
                return []
            raise

    @staticmethod
    def _normalize_user(user: Any) -> Any:
        if not isinstance(user, dict):
            return user
        username = user.get("username") or user.get("name") or user.get("email", "")
        full_name = user.get("fullName") or user.get("displayName") or username
        return {**user, "username": username, "fullName": full_name}
