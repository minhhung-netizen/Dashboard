from __future__ import annotations

import json
import re
from typing import Any


def parse_forgiving_json(text: str) -> dict[str, Any]:
    attempts = []
    stripped = text.strip()
    if stripped:
        attempts.append(stripped)
    if stripped.startswith("="):
        attempts.append(stripped[1:].strip())

    repaired = re.sub(r'("[^"]+"\s*):\s*=', r"\1:", stripped)
    if repaired != stripped:
        attempts.append(repaired)
    if repaired.startswith("="):
        attempts.append(repaired[1:].strip())

    seen: set[str] = set()
    for candidate in attempts:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            raise ValueError("Webhook body must be a JSON object")
        return data
    raise ValueError("Invalid webhook JSON")
