from typing import Any, Self

import httpx

from jsm._http import create_basic_client, request_json

EXPERIMENTAL_HEADERS = {"X-ExperimentalApi": "opt-in"}


class Assets:
    """Jira Service Management Assets API client."""

    def __init__(self, workspace_id: str, auth: dict[str, Any]) -> None:
        self._workspace_id = workspace_id
        self._auth = auth
        base = auth["url"].rstrip("/")
        self._base_url = f"{base}/gateway/api/jsm/assets/workspace/{workspace_id}/v1"
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        self._client = create_basic_client(
            self._auth,
            base_url=self._base_url,
            extra_headers=EXPERIMENTAL_HEADERS,
        )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _client_or_raise(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Use 'async with Assets(...)' before calling API methods")
        return self._client

    async def _get(self, path: str) -> Any:
        return await request_json(self._client_or_raise(), "GET", path)

    async def _post(self, path: str, *, json: dict[str, Any]) -> Any:
        return await request_json(self._client_or_raise(), "POST", path, json=json)

    async def get_object(self, object_id: str) -> Any:
        return await self._get(f"/object/{object_id}")

    async def get_object_attributes(self, object_id: str) -> Any:
        return await self._get(f"/object/{object_id}/attributes")

    async def get_object_history(self, object_id: str) -> Any:
        return await self._get(f"/object/{object_id}/history")

    async def get_object_reference_info(self, object_id: str) -> Any:
        return await self._get(f"/object/{object_id}/referenceinfo")

    async def get_object_connected_tickets(self, object_id: str) -> Any:
        return await self._get(f"/objectconnectedtickets/{object_id}/tickets")

    async def post_object_aql(self, query: str) -> Any:
        return await self._post("/object/aql", json={"qlQuery": query})

    async def post_object_navlist_aql(self, query: str) -> Any:
        return await self._post("/object/navlist/aql", json={"qlQuery": query})

    async def list_object_schema(self) -> Any:
        return await self._get("/objectschema/list")

    async def get_object_schema(self, object_schema_id: str) -> Any:
        return await self._get(f"/objectschema/{object_schema_id}")

    async def get_object_schema_attributes(self, object_schema_id: str) -> Any:
        return await self._get(f"/objectschema/{object_schema_id}/attributes")

    async def get_object_schema_objecttypes(self, object_schema_id: str, flat: bool = False) -> Any:
        url = f"/objectschema/{object_schema_id}/objecttypes"
        if flat:
            url += "/flat"
        return await self._get(url)

    async def get_object_type(self, object_type_id: str) -> Any:
        return await self._get(f"/objecttype/{object_type_id}")

    async def get_object_type_attributes(self, object_type_id: str) -> Any:
        return await self._get(f"/objecttype/{object_type_id}/attributes")

    async def list_config_status_type(self) -> Any:
        return await self._get("/config/statustype")

    async def get_config_status_type(self, status_type_id: str) -> Any:
        return await self._get(f"/config/statustype/{status_type_id}")
