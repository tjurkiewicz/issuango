import pytest

_password = 'password'

@pytest.fixture
def user(db, django_user_model, django_username_field):
    UserModel = django_user_model
    username_field = django_username_field

    try:
        user = UserModel._default_manager.get(**{username_field: 'admin'})
    except UserModel.DoesNotExist:
        extra_fields = {}
        if username_field != 'username':
            extra_fields[username_field] = 'admin'
        user = UserModel._default_manager.create_user(
            'admin', 'admin@example.com', _password, **extra_fields)
    return user


@pytest.fixture()
def user_client(db, user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.login(username=user.username, password=_password)
    return client