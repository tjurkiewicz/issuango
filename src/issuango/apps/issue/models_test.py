
import django.contrib.auth
import pytest

import models


@pytest.fixture
def user():
    User = django.contrib.auth.get_user_model()
    return User.objects.create_user('john', 'john@example.com', 'password')

@pytest.fixture
def project():
    issue_class = models.IssueClass()
    issue_class.save()

    project = models.Project(issue_class=issue_class)
    project.save()
    return project


@pytest.mark.django_db
def test_issue_auto_now(user, project):
    issue = models.Issue(reporter=user, project=project)
    issue.save()

    assert issue.created <= issue.updated