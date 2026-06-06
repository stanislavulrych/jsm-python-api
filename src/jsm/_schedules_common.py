from typing import Any

OPS_AUTH_HINT = (
    " Check API token has JSM Ops scope read:ops-config:jira-service-management "
    "(classic token from id.atlassian.com, or scoped token with Bearer via use_bearer)."
)


def unwrap_response(resp: Any) -> Any:
    if isinstance(resp, dict) and "data" in resp:
        return resp["data"]
    return resp


def normalize_user(user: Any) -> Any:
    if not isinstance(user, dict):
        return user
    username = user.get("username") or user.get("name") or user.get("email", "")
    full_name = user.get("fullName") or user.get("displayName") or username
    return {**user, "username": username, "fullName": full_name}


def build_timeline_params(
    *,
    identifier_type: str | None,
    expand: bool | str | None,
    interval: int | None,
    interval_unit: str | None,
    date: str | None,
) -> dict[str, Any]:
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
    return params
