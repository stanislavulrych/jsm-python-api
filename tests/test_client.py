import httpx

from jsm import Schedules_v1


def _auth() -> dict[str, str]:
    return {
        "cloud_id": "test-cloud",
        "username": "user@example.com",
        "password": "token",
    }


def test_get_users_normalizes_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/users"):
            return httpx.Response(
                200,
                json={"data": {"values": [{"email": "a@b.com", "displayName": "Alice"}]}},
            )
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    with Schedules_v1(auth=_auth()) as client:
        client._client = httpx.Client(
            transport=transport,
            base_url=client._base_url,
            auth=httpx.BasicAuth("user@example.com", "token"),
        )
        users = client.get_users()
    assert users[0]["username"] == "a@b.com"
    assert users[0]["fullName"] == "Alice"
