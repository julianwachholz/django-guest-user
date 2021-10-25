import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
@pytest.mark.django_db
def authenticated_client(client):
    UserModel = get_user_model()
    user = UserModel.objects.create_user(username="registered_user")
    client.force_login(user)
    return client
