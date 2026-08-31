from __future__ import annotations

import json
import re
from typing import Any


def parse_forgiving_json(text: str) -> dict[str, Any]:
    attempts = []
    stripped = text.strip()
    if stripped:
        attempts.append(stripped)
    unwrapped = _unwrap_misquoted_json(stripped)
    if unwrapped != stripped:
        attempts.append(unwrapped)
    if stripped.startswith("="):
        attempts.append(stripped[1:].strip())

    for base in (stripped, unwrapped):
        repaired = re.sub(r'("[^"]+"\s*):\s*=', r"\1:", base)
        if repaired != base:
            attempts.append(repaired)
        if repaired.startswith("="):
            attempts.append(repaired[1:].strip())

    seen: set[str] = set()
    index = 0
    while index < len(attempts):
        candidate = attempts[index]
        index += 1
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(data, str):
            nested = data.strip()
            nested_unwrapped = _unwrap_misquoted_json(nested)
            for value in (nested, nested_unwrapped):
                if value and value not in seen:
                    attempts.append(value)
                repaired = re.sub(r'("[^"]+"\s*):\s*=', r"\1:", value)
                if repaired and repaired not in seen:
                    attempts.append(repaired)
            continue
        if not isinstance(data, dict):
            raise ValueError("Webhook body must be a JSON object")
        return data
    raise ValueError("Invalid webhook JSON")


def _unwrap_misquoted_json(value: str) -> str:
    candidate = value.strip()
    if candidate.startswith('"') and candidate[1:].lstrip().startswith("{"):
        candidate = candidate[1:].lstrip()
    if candidate.endswith('"') and candidate.rstrip('"').rstrip().endswith("}"):
        candidate = candidate[:-1].rstrip()
    return candidate
