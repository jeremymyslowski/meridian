import json
import os
from pathlib import Path

def _resolve_flags_path() -> Path:
    if env_path := os.getenv("FEATURE_FLAGS_PATH"):
        return Path(env_path)
    candidates = [
        Path(__file__).resolve().parents[3] / "packages" / "config" / "feature-flags.json",
        Path("/packages/config/feature-flags.json"),
        Path(__file__).resolve().parents[1] / "feature-flags.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]

_default_flags = {
    "analytics_dashboard": True,
    "file_attachments": True,
    "webhook_integrations": True,
    "task_pagination": True,
    "dark_mode": False,
}


def load_feature_flags() -> dict[str, bool]:
    path = _resolve_flags_path()
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return _default_flags.copy()