import logging
from typing import Any, Self

import httpx

from jsm._http import create_basic_client, request_json
from jsm._schedules_common import (
    OPS_AUTH_HINT,
    build_timeline_params,
    normalize_user,
    unwrap_response,
)

logger = logging.getLogger("jsm")


class AsyncSchedules_v1:  # noqa: N801
    """Async Jira Service Management operations (on-call) schedules API."""

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
            raise RuntimeError("Use 'async with AsyncSchedules_v1(...)' before calling API methods")
        return self._client

    async def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> Any:
        client = self._client_or_raise()
        hint = OPS_AUTH_HINT if method == "GET" else ""
        return await request_json(client, method, path, params=params, hint=hint)

    async def _get_paginated_values(self, path: str, params: dict[str, Any] | None = None) -> Any:
        params = dict(params or {})
        size = min(params.pop("size", 50), 50)
        results: list[Any] = []
        offset = 0
        while True:
            resp = unwrap_response(
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
        return unwrap_response(await self._request("GET", path, params=params))

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
        params = build_timeline_params(
            identifier_type=identifier_type or identifierType,
            expand=expand,
            interval=interval,
            interval_unit=interval_unit or intervalUnit,
            date=date,
        )
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
            return normalize_user(user)
        try:
            users = await self._get_paginated_values(url)
            return [normalize_user(u) for u in users]
        except httpx.HTTPStatusError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                logger.warning(
                    "JSM Ops API: /users endpoint not available (404); "
                    "user display names will fall back to email addresses."
                )
                return []
            raise
