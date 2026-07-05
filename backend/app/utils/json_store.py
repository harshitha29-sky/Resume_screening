import json
from typing import Any


def dumps(value: Any) -> str:
    return json.dumps(value or [])


def loads(value: str | None, default: Any = None) -> Any:
    if not value:
        return [] if default is None else default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return [] if default is None else default
