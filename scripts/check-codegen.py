#!/usr/bin/env python3
"""Verify OpenAPI spec, api-client, and contract manifest stay in sync."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPENAPI_PATH = ROOT / "docs/api/openapi.yaml"
MANIFEST_PATH = ROOT / "packages/api-client/contract-manifest.json"
CLIENT_PATH = ROOT / "packages/api-client/src/index.ts"

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


def load_openapi_operations() -> set[tuple[str, str]]:
    operations: set[tuple[str, str]] = set()
    current_path: str | None = None

    for line in OPENAPI_PATH.read_text().splitlines():
        path_match = re.match(r"^  (/api/[^:]+):\s*$", line)
        if path_match:
            current_path = path_match.group(1)
            continue

        method_match = re.match(r"^    ([a-z]+):\s*$", line)
        if method_match and current_path:
            method = method_match.group(1)
            if method in HTTP_METHODS:
                operations.add((method.upper(), current_path))

    return operations


def load_manifest_operations() -> list[dict[str, str]]:
    manifest = json.loads(MANIFEST_PATH.read_text())
    return manifest["operations"]


def openapi_path_to_client_fragment(path: str) -> str:
    parts = path.split("/")
    fragments: list[str] = []
    for part in parts:
        if part.startswith("{") and part.endswith("}"):
            param = part[1:-1]
            camel = "".join(
                word.capitalize() if index else word
                for index, word in enumerate(param.split("_"))
            )
            fragments.append(f"${{{camel}}}")
        elif part:
            fragments.append(part)
    return "/" + "/".join(fragments)


def main() -> int:
    errors: list[str] = []

    openapi_ops = load_openapi_operations()
    manifest_ops = load_manifest_operations()
    manifest_set = {(op["method"], op["path"]) for op in manifest_ops}

    missing_from_manifest = sorted(openapi_ops - manifest_set)
    extra_in_manifest = sorted(manifest_set - openapi_ops)
    if missing_from_manifest:
        errors.append(
            "OpenAPI operations missing from contract-manifest.json:\n  "
            + "\n  ".join(f"{method} {path}" for method, path in missing_from_manifest)
        )
    if extra_in_manifest:
        errors.append(
            "contract-manifest.json has operations not in OpenAPI:\n  "
            + "\n  ".join(f"{method} {path}" for method, path in extra_in_manifest)
        )

    client_source = CLIENT_PATH.read_text()
    for op in manifest_ops:
        method = op["method"]
        path = op["path"]
        client_method = op["client_method"]
        path_fragment = openapi_path_to_client_fragment(path)

        if f"{client_method}(" not in client_source:
            errors.append(f"api-client missing method {client_method}() for {method} {path}")
            continue

        if path_fragment not in client_source:
            errors.append(
                f"api-client.{client_method}() missing path fragment {path_fragment!r} "
                f"for {method} {path}"
            )
            continue

        if method != "GET":
            method_pattern = re.compile(
                rf"{re.escape(client_method)}\([^)]*\)[\s\S]*?method:\s*['\"]{method}['\"]",
                re.MULTILINE,
            )
            if not method_pattern.search(client_source):
                errors.append(
                    f"api-client.{client_method}() should use HTTP {method} for {path}"
                )

    if errors:
        print("Codegen contract check failed:\n")
        for error in errors:
            print(f"- {error}\n")
        return 1

    print(
        f"OK: {len(openapi_ops)} OpenAPI operations match manifest and @meridian/api-client"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())