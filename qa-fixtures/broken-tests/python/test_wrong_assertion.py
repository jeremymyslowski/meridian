"""Broken test: wrong expected HTTP status."""

from status_codes import login_response_code


def test_login_returns_200():
    # BUG in test: login_response_code() returns 200 but test expected 201
    assert login_response_code() == 201