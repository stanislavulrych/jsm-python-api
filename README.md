# Jira Service Management Python Bindings

Async Python bindings for Jira Service Management API.

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
import asyncio

from jsm import Schedules


async def main():
    async with Schedules(
        auth={
            "cloud_id": "<your-cloud-id>",
            "username": "you@example.com",
            "password": "<api-token>",
        },
    ) as schedules:
        users = await schedules.get_users()
        schedules_list = await schedules.get_schedules()
        timeline = await schedules.get_schedule_timeline(
            "<schedule-id>",
            expand=True,
            date="2026-05-01T00:00:00+02:00",
            interval_unit="days",
            interval=33,
        )
        print(users, schedules_list, timeline)


asyncio.run(main())
```

### Assets API

```python
import asyncio

from jsm import Assets


async def main():
    async with Assets(
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
| `from jiraservicemanagement.api.v1 import Schedules` | `from jsm import Schedules` |
| `schedules.get_users()` | `await schedules.get_users()` |
| `Assets(workspaceId=...)` | `Assets(workspace_id=...)` |
| `atlassian-python-api` | `httpx` |

## Contributing

Contribution is welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
