from typing import Any, Self

import httpx

from jsm._http import create_basic_sync_client, request_json_sync

EXPERIMENTAL_HEADERS = {"X-ExperimentalApi": "opt-in"}


class Assets_v1:  # noqa: N801
    """Synchronous Jira Service Management Assets API client."""

    def __init__(self, workspace_id: str, auth: dict[str, Any]) -> None:
        self._workspace_id = workspace_id
        self._auth = auth
        base = auth["url"].rstrip("/")
        self._base_url = f"{base}/gateway/api/jsm/assets/workspace/{workspace_id}/v1"
        self._client: httpx.Client | None = create_basic_sync_client(
            self._auth,
            base_url=self._base_url,
            extra_headers=EXPERIMENTAL_HEADERS,
        )

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _client_or_raise(self) -> httpx.Client:
        if self._client is None:
            raise RuntimeError("Assets_v1 is closed")
        return self._client

    def _get(self, path: str) -> Any:
        return request_json_sync(self._client_or_raise(), "GET", path)

    def _post(self, path: str, *, json: dict[str, Any]) -> Any:
        return request_json_sync(self._client_or_raise(), "POST", path, json=json)

    def get_object(self, object_id: str) -> Any:
        return self._get(f"/object/{object_id}")

    def get_object_attributes(self, object_id: str) -> Any:
        return self._get(f"/object/{object_id}/attributes")

    def get_object_history(self, object_id: str) -> Any:
        return self._get(f"/object/{object_id}/history")

    def get_object_reference_info(self, object_id: str) -> Any:
        return self._get(f"/object/{object_id}/referenceinfo")

    def get_object_connected_tickets(self, object_id: str) -> Any:
        return self._get(f"/objectconnectedtickets/{object_id}/tickets")

    def post_object_aql(self, query: str) -> Any:
        return self._post("/object/aql", json={"qlQuery": query})

    def post_object_navlist_aql(self, query: str) -> Any:
        return self._post("/object/navlist/aql", json={"qlQuery": query})

    def list_object_schema(self) -> Any:
        return self._get("/objectschema/list")

    def get_object_schema(self, object_schema_id: str) -> Any:
        return self._get(f"/objectschema/{object_schema_id}")

    def get_object_schema_attributes(self, object_schema_id: str) -> Any:
        return self._get(f"/objectschema/{object_schema_id}/attributes")

    def get_object_schema_objecttypes(self, object_schema_id: str, flat: bool = False) -> Any:
        url = f"/objectschema/{object_schema_id}/objecttypes"
        if flat:
            url += "/flat"
        return self._get(url)

    def get_object_type(self, object_type_id: str) -> Any:
        return self._get(f"/objecttype/{object_type_id}")

    def get_object_type_attributes(self, object_type_id: str) -> Any:
        return self._get(f"/objecttype/{object_type_id}/attributes")

    def list_config_status_type(self) -> Any:
        return self._get("/config/statustype")

    def get_config_status_type(self, status_type_id: str) -> Any:
        return self._get(f"/config/statustype/{status_type_id}")
