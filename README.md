# Jira Service Management Python Bindings

Low-level Python bindings for Jira Service Management API.

Jira Service Management API documentation can be found at https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/


## Installation

Install current release by pip

```
pip install jsm-python-api
```

## Getting Started

You need an API token for communicating with Opsgenie REST APIs. 


### Assets API

```
from jiraservicemanagement.api.v1 import Assets

assets = Assets(
    workspaceId="...", 
    auth={
        "url": "...",
        "username": "...",
        "password": "..."
    }
)
object_schema = assets.list_object_schema()
print(object_schema)

```


## Contributing

Contribution is welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
