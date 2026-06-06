import httpx
import pytest

from jsm import AsyncAssets_v1


@pytest.mark.asyncio
async def test_list_object_schema_sends_experimental_header() -> None:
    seen_headers: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen_headers.update(dict(request.headers))
        return httpx.Response(200, json={"values": []})

    transport = httpx.MockTransport(handler)
    auth = {
        "url": "https://example.atlassian.net/",
        "username": "user@example.com",
        "password": "token",
    }
    async with AsyncAssets_v1(workspace_id="ws-1", auth=auth) as assets:
        assets._client = httpx.AsyncClient(
            transport=transport,
            base_url=assets._base_url,
            auth=httpx.BasicAuth("user@example.com", "token"),
            headers={"X-ExperimentalApi": "opt-in"},
        )
        result = await assets.list_object_schema()
    assert result == {"values": []}
    assert seen_headers.get("x-experimentalapi") == "opt-in"
