from typing import Any

import httpx

DEFAULT_TIMEOUT = 75.0
JSON_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def raise_for_status(response: httpx.Response, url: str, *, hint: str = "") -> None:
    if response.is_success:
        return
    body = (response.text or "").strip()[:2000]
    raise httpx.HTTPStatusError(
        f"HTTP {response.status_code} {response.reason_phrase} for {url}: {body or '(empty body)'}{hint}",
        request=response.request,
        response=response,
    )


def parse_json(response: httpx.Response) -> Any:
    if not response.text:
        return {}
    return response.json()


async def request_json(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    *,
    hint: str = "",
    **kwargs: Any,
) -> Any:
    response = await client.request(method, url, **kwargs)
    raise_for_status(response, url, hint=hint)
    return parse_json(response)


def create_basic_client(
    auth: dict[str, Any],
    *,
    base_url: str,
    extra_headers: dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.AsyncClient:
    headers = dict(JSON_HEADERS)
    if extra_headers:
        headers.update(extra_headers)

    token = auth.get("password") or auth.get("token", "")
    client_kwargs: dict[str, Any] = {
        "base_url": base_url.rstrip("/"),
        "headers": headers,
        "timeout": timeout,
    }
    if auth.get("use_bearer"):
        headers["Authorization"] = f"Bearer {token}"
    else:
        client_kwargs["auth"] = httpx.BasicAuth(auth["username"], token)

    return httpx.AsyncClient(**client_kwargs)
