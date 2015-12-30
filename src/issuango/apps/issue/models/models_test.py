
import pytest

import models



@pytest.mark.parametrize('Model', [
    models.Project,
    models.IssueClass,
])
def test_str(Model):
    instance = Model(name='name')
    assert str(instance) == '<{0}>'.format(instance.name)


@pytest.mark.django_db
def test_issue_auto_now(issue):
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
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    attr = attribute(issue.issue_class, models.Attribute.OPTION, option_group=option_group)

    option = models.AttributeOption(group=option_group, option='option')
    option.save()

    issue.attr.code = option
    issue.save()

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr).value == option

@pytest.mark.django_db
def test_set_option_by_string(issue, attribute):
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    attr = attribute(issue.issue_class, models.Attribute.OPTION, option_group=option_group)

    option_name = 'option'
    option = models.AttributeOption(group=option_group, option=option_name)
    option.save()

    issue.attr.code = option_name
    issue.save()

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr).value == option
