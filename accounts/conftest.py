import pytest
from accounts.models import User

@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        return User.objects.create(**kwargs)
    return create_user
