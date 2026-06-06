# Jira Service Management Python Bindings

Sync and async Python bindings for Jira Service Management API.

- Service desk: https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/
- Operations (schedules, on-call): https://developer.atlassian.com/cloud/jira/service-desk-ops/rest/v2/intro/

## Requirements

Python >= 3.12.

## Installation

```bash
uv add jsm-python-api
```

Runtime dependency: `httpx` only.

## Development

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
```

## Getting Started

You need Jira Cloud credentials (email + API token) and your site `cloud_id` for the operations API.

### Schedules API (JSM Ops)

Replacement for `opsgenie.Schedules` after migrating on-call to Jira Service Management:

```python
from jsm import Schedules_v1

auth = {
    "cloud_id": "<your-cloud-id>",
    "username": "you@example.com",
    "password": "<api-token>",
}

with Schedules_v1(auth=auth) as client:
    users = client.get_users()
    schedules_list = client.get_schedules()
    timeline = client.get_schedule_timeline(
        "<schedule-id>",
        expand=True,
        date="2026-05-01T00:00:00+02:00",
        interval_unit="days",
        interval=33,
    )
```

Async equivalent: `from jsm import AsyncSchedules_v1` with `async with` / `await`.

### Assets API

```python
import asyncio

from jsm import AsyncAssets_v1


async def main():
    async with AsyncAssets_v1(
        workspace_id="...",
        auth={
            "url": "https://yoursite.atlassian.net/",
            "username": "...",
            "password": "...",
        },
    ) as assets:
        object_schema = await assets.list_object_schema()
        print(object_schema)


asyncio.run(main())
```

## Breaking changes in v0.3.0

| Before | After |
|--------|-------|
| `from jiraservicemanagement.api.v1 import Schedules` | `from jsm import Schedules_v1` or `AsyncSchedules_v1` |
| `schedules.get_users()` | `client.get_users()` or `await client.get_users()` |
| `Assets(workspaceId=...)` | `Assets_v1(workspace_id=...)` / `AsyncAssets_v1(workspace_id=...)` |
| `atlassian-python-api` | `httpx` |

## Contributing

Contribution is welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
