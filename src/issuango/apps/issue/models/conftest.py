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
def attribute_scheme():
    attribute_scheme = models.AttributeScheme(name='Basic issue class')
    attribute_scheme.save()
    return attribute_scheme

@pytest.fixture
def project(attribute_scheme):
    project = models.Project(attribute_scheme=attribute_scheme, name='project name')
    project.save()
    return project

@pytest.fixture
def issue(project, user, status):
    issue = models.Issue.objects.create(project=project, reporter=user, status=status)
    return issue

@pytest.fixture
def project_role(project, user):
    project_role = models.ProjectRole(project=project, user=user, role=models.ProjectRole.READ_ROLE)
    project_role.save()
    return project_role


@pytest.fixture
def attribute():
    def fixture(attribute_scheme, type, name='name', code='code', **kwargs):
        a = models.Attribute(name=name, code=code, type=type, **kwargs)
        a.save()
        a.attribute_scheme.add(attribute_scheme)
        return a
    return fixture
