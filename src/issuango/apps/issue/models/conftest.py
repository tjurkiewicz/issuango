import django.contrib.auth
import pytest

import models

@pytest.fixture
def status():
    status = models.IssueStatus(name='initial')
    status.save()
    return status

@pytest.fixture
def user():
    User = django.contrib.auth.get_user_model()
    return User.objects.create_user('john', 'john@example.com', 'password')

@pytest.fixture
def project():
    project = models.Project(issue_class=issue_class())
    project.save()
    return project


@pytest.fixture
def issue_class():
    issue_class = models.IssueClass(name='Basic issue class')
    issue_class.save()
    return issue_class


@pytest.fixture
def issue():
    issue = models.Issue(project=project(), reporter=user(), status=status())
    issue.save()
    return issue

@pytest.fixture
def attribute():
    def fixture(issue_class, type, name='name', code='code', **kwargs):
        a = models.Attribute(issue_class=issue_class, name=name, code=code, type=type, **kwargs)
        a.save()
        return a
    return fixture
