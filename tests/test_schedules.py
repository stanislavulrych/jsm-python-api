import httpx
import pytest

from jsm import Schedules


def _auth() -> dict[str, str]:
    return {
        "cloud_id": "test-cloud",
        "username": "user@example.com",
        "password": "token",
    }


@pytest.mark.asyncio
async def test_get_users_normalizes_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/users"):
            return httpx.Response(
                200,
                json={"data": {"values": [{"email": "a@b.com", "displayName": "Alice"}]}},
            )
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    async with Schedules(auth=_auth()) as schedules:
        schedules._client = httpx.AsyncClient(
            transport=transport,
            base_url=schedules._base_url,
            auth=httpx.BasicAuth("user@example.com", "token"),
        )
        users = await schedules.get_users()
    assert users[0]["username"] == "a@b.com"
    assert users[0]["fullName"] == "Alice"


@pytest.mark.asyncio
async def test_get_users_returns_empty_on_404() -> None:
    transport = httpx.MockTransport(lambda _request: httpx.Response(404, text="not found"))
    async with Schedules(auth=_auth()) as schedules:
        schedules._client = httpx.AsyncClient(
            transport=transport,
            base_url=schedules._base_url,
            auth=httpx.BasicAuth("user@example.com", "token"),
        )
        users = await schedules.get_users()
    assert users == []
