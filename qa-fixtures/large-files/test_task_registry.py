import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from task_registry import normalize_task_title


def test_normalize_task_title_strips_and_collapses():
    assert normalize_task_title("  hello   world  ") == "hello world"


def test_normalize_task_title_already_clean():
    assert normalize_task_title("hello world") == "hello world"