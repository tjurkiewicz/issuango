
import django.contrib.auth
import pytest

import models


@pytest.fixture
def user():
    User = django.contrib.auth.get_user_model()
    return User.objects.create_user('john', 'john@example.com', 'password')


@pytest.mark.django_db
def test_issue_auto_now(user):
    issue = models.Issue(reporter=user)
    issue.save()

    assert issue.created <= issue.updated