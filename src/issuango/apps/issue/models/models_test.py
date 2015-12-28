
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

@pytest.fixture
def attribute():
    def fixture(issue_class, type, name='name', code='code'):
        a = models.Attribute(issue_class=issue_class, name=name, code=code, type=type)
        a.save()
        return a
    return fixture


@pytest.mark.parametrize('Model', [
    models.Project,
    models.IssueClass,
])
def test_str(Model):
    instance = Model(name='name')
    assert str(instance) == '<{0}>'.format(instance.name)


@pytest.mark.django_db
def test_issue_auto_now(user, project):
    issue = models.Issue(reporter=user, project=project)
    issue.save()

    assert issue.created <= issue.updated

@pytest.mark.parametrize('value,type', [
    ('text', models.Attribute.TEXT,),
    (123, models.Attribute.INTEGER,),
    (False, models.Attribute.BOOLEAN,),
    (True, models.Attribute.BOOLEAN,),
])
@pytest.mark.django_db
def test_attribute(issue, value, type, attribute):
    attr = attribute(issue.project.issue_class, type)

    issue.attr.code = value
    issue.save()

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr) is not None
    assert models.Issue.objects.last().attr.code == value


@pytest.mark.parametrize('value,type', [
    ('text', models.Attribute.TEXT,),
    (123, models.Attribute.INTEGER,),
    (None, models.Attribute.BOOLEAN,),
    (False, models.Attribute.BOOLEAN,),
    (True, models.Attribute.BOOLEAN,),
])
@pytest.mark.django_db
def test_delete_attribute(issue, attribute, value, type):
    attr = attribute(issue.project.issue_class, type)

    issue.attr.code = value
    issue.save()

    issue.attr.code = None
    issue.save()

    with pytest.raises(models.AttributeValue.DoesNotExist):
        models.AttributeValue.objects.get(issue=issue, attribute=attr)

    assert getattr(models.Issue.objects.last().attr, 'code', None) is None


@pytest.mark.parametrize('value,type', [
    (None, models.Attribute.TEXT,),
    (None, models.Attribute.INTEGER,),
])
@pytest.mark.django_db
def test_no_attribute(issue, attribute, value, type):
    attribute(issue.project.issue_class, type, code='code')

    issue.attr.code = value
    issue.save()

    assert not hasattr(models.Issue.objects.last().attr, 'code')


@pytest.mark.django_db
def test_bad_integer_attribute(issue, attribute):
    attr = attribute(issue.project.issue_class, models.Attribute.INTEGER)

    with pytest.raises(ValueError):
        attribute_value = models.AttributeValue(issue=issue, attribute=attr)
        attribute_value.value = 'text'
        attribute_value.save()


@pytest.mark.django_db
def test_attribute_option_group_is_selected_iff_type_is_selected(issue, attribute):
    attr = attribute(issue.issue_class, models.Attribute.OPTION)

    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    option = models.AttributeOption(group=option_group, option='option')
    option.save()

    issue.attr.code = option
    issue.save()

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr).value == option
