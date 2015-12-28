import pickle

import django.contrib.auth
import pytest

import models
import utils


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
    issue = models.Issue(project=project(), reporter=user())
    issue.save()
    return issue


@pytest.mark.django_db
def test_pickle(issue):
    iac = utils.IssueAttributesContainer(issue)

    pickled = pickle.dumps(iac)
    new_iac = pickle.loads(pickled)

    assert new_iac.issue == issue