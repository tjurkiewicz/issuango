
import django.contrib.auth
import pytest

import models


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
def test_issue_auto_now(user, project):
    issue = models.Issue(reporter=user, project=project)
    issue.save()

    assert issue.created <= issue.updated

@pytest.mark.parametrize('value,type', [
    ('text', models.Attribute.TEXT,),
    (123, models.Attribute.INTEGER,),
    (None, models.Attribute.BOOLEAN,),
    (False, models.Attribute.BOOLEAN,),
    (True, models.Attribute.BOOLEAN,),
])
@pytest.mark.django_db
def test_attribute(issue, value, type):
    attribute = models.Attribute(issue_class=issue.project.issue_class, type=type, name='name', code='code')
    attribute.save()

    issue.attr.code = value
    issue.save()

    assert models.Issue.objects.last().attr.code == value


@pytest.mark.django_db
def test_bad_integer_attribute(issue):
    attribute = models.Attribute(issue_class=issue.project.issue_class, type=models.Attribute.INTEGER, name='name', code='code')
    attribute.save()

    with pytest.raises(ValueError):
        attribute_value = models.AttributeValue(issue=issue, attribute=attribute)
        attribute_value.value = 'text'
        attribute_value.save()


@pytest.mark.django_db
def test_attribute_option_group_is_selected_iff_type_is_selected(issue_class):
    attribute = models.Attribute(issue_class=issue_class)
    attribute.name = 'name'
    attribute.code = 'code'
    attribute.type = models.Attribute.OPTION

    assert False