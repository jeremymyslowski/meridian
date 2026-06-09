import pytest


@pytest.fixture
def seeded_user():
    return {"email": "user1@example.com", "name": "User 1"}