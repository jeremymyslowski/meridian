"""Module B — circular import fixture."""

from module_a import get_a_value  # noqa: E402 — intentional trap

VALUE_B = "b"


def get_b_value() -> str:
    return get_a_value() + VALUE_B