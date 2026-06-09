"""Module A — circular import fixture."""

from module_b import get_b_value  # noqa: E402 — intentional trap

VALUE_A = "a"


def get_a_value() -> str:
    return VALUE_A