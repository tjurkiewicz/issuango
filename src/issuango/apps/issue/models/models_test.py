import datetime

import django.core.validators
import django.utils.timezone
import freezegun
import pytest

import models


@pytest.mark.django_db
def test_project_str(project):
    assert str(project) == '<{0}>'.format(project.name)


@pytest.mark.django_db
def test_attribute_scheme_str(attribute_scheme):
    assert str(attribute_scheme) == '<{0}>'.format(attribute_scheme.name)

@pytest.mark.django_db
def test_project_role_str(project_role):
    assert str(project_role) == '<{}@{}: {}>'.format(project_role.user, project_role.project.name, project_role.role)



@pytest.mark.django_db
def test_issue_auto_now(issue):
    assert issue.created <= issue.updated

@freezegun.freeze_time('2000-01-01 00:00:00')
@pytest.mark.parametrize('repeat', [1,2])
@pytest.mark.parametrize('value,type', [
    ('text', models.Attribute.TEXT,),
    (123, models.Attribute.INTEGER,),
    (False, models.Attribute.BOOLEAN,),
    (True, models.Attribute.BOOLEAN,),
    (django.utils.timezone.now(), models.Attribute.DATE,),
])
@pytest.mark.django_db
def test_attribute(issue, attribute, value, type, repeat):
    attr = attribute(issue.project.attribute_scheme, type)

    while repeat:
        issue.attr.code = value
        issue.clean()
        issue.save()
        repeat -= 1

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr).value == value
    assert models.Issue.objects.last().attr.code == value


@pytest.mark.parametrize('value,new_value,type', [
    ('text', 'text2', models.Attribute.TEXT,),
    (123, 1234, models.Attribute.INTEGER,),
    (False, True, models.Attribute.BOOLEAN,),
])
@pytest.mark.django_db
def test_update_attribute(issue, attribute, value, new_value, type):
    attr = attribute(issue.project.attribute_scheme, type)

    issue.attr.code = value
    issue.clean()
    issue.save()

    issue.attr.code = new_value
    issue.clean()
    issue.save()

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr).value == new_value
    assert models.Issue.objects.last().attr.code == new_value



@pytest.mark.parametrize('value,type', [
    ('text', models.Attribute.TEXT,),
    (123, models.Attribute.INTEGER,),
    (None, models.Attribute.BOOLEAN,),
    (False, models.Attribute.BOOLEAN,),
    (True, models.Attribute.BOOLEAN,),
])
@pytest.mark.django_db
def test_delete_attribute(issue, attribute, value, type):
    attr = attribute(issue.project.attribute_scheme, type)

    issue.attr.code = value
    issue.clean()
    issue.save()

    issue.attr.code = None
    issue.clean()
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
    attribute(issue.project.attribute_scheme, type, code='code')

    issue.attr.code = value
    issue.clean()
    issue.save()

    assert not hasattr(models.Issue.objects.last().attr, 'code')


@pytest.mark.parametrize('bad_value,type', [
    (123, models.Attribute.TEXT),
    ('a', models.Attribute.FLOAT),
    ('a', models.Attribute.INTEGER),
    ('a', models.Attribute.DATE),
    ('a', models.Attribute.BOOLEAN),
])
@pytest.mark.django_db
def test_validators(issue, attribute, bad_value, type):
    attr = attribute(issue.project.attribute_scheme, type)

    with pytest.raises(django.core.validators.ValidationError):
        attr.validate_value(bad_value)


@pytest.mark.parametrize('type', [
    models.Attribute.TEXT,
    models.Attribute.FLOAT,
    models.Attribute.INTEGER,
    models.Attribute.DATE,
    models.Attribute.BOOLEAN,
])
@pytest.mark.django_db
def test_required_attribute(issue, attribute, type):
    attribute(issue.project.attribute_scheme, type, required=True)

    with pytest.raises(django.core.validators.ValidationError):
        issue.attr.code = None
        issue.clean()


@pytest.mark.django_db
def test_bad_integer_attribute(issue, attribute):
    attr = attribute(issue.project.attribute_scheme, models.Attribute.INTEGER)

    with pytest.raises(ValueError):
        attribute_value = models.AttributeValue(issue=issue, attribute=attr)
        attribute_value.value = 'text'
        attribute_value.save()


@pytest.mark.django_db
def test_attribute_option_group_is_selected_iff_type_is_selected(issue, attribute):
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    attr = attribute(issue.attribute_scheme, models.Attribute.OPTION, option_group=option_group)

    option = models.AttributeOption(group=option_group, option='option')
    option.save()

    issue.attr.code = option
    issue.clean()
    issue.save()

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr).value == option

@pytest.mark.django_db
def test_set_option_by_string(issue, attribute):
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    attr = attribute(issue.attribute_scheme, models.Attribute.OPTION, option_group=option_group)

    option_name = 'option'
    option = models.AttributeOption(group=option_group, option=option_name)
    option.save()

    issue.attr.code = option_name
    issue.clean()
    issue.save()

    assert models.AttributeValue.objects.get(issue=issue, attribute=attr).value == option

@pytest.mark.django_db
def test_set_bad_option_by_string(issue, attribute):
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    attribute(issue.attribute_scheme, models.Attribute.OPTION, option_group=option_group)

    option_name = 'option'
    option = models.AttributeOption(group=option_group, option=option_name)
    option.save()

    with pytest.raises(django.core.validators.ValidationError):
        issue.attr.code = 'bad_option'
        issue.clean()

@pytest.mark.django_db
def test_set_not_an_option(issue, attribute):
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    attribute(issue.attribute_scheme, models.Attribute.OPTION, option_group=option_group)

    with pytest.raises(django.core.validators.ValidationError):
        issue.attr.code = issue
        issue.clean()

@pytest.mark.django_db
def test_set_unsaved_option(issue, attribute):
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    attribute(issue.attribute_scheme, models.Attribute.OPTION, option_group=option_group)

    option_name = 'option'
    option = models.AttributeOption(group=option_group, option=option_name)

    with pytest.raises(django.core.validators.ValidationError):
        issue.attr.code = option
        issue.clean()


@pytest.mark.django_db
def test_set_unrelated_option(issue, attribute):
    option_group = models.AttributeOptionGroup(name='option_group')
    option_group.save()

    option_group2 = models.AttributeOptionGroup(name='option_group2')
    option_group2.save()

    attribute(issue.attribute_scheme, models.Attribute.OPTION, option_group=option_group, name='name', code='code')
    attribute(issue.attribute_scheme, models.Attribute.OPTION, option_group=option_group2, name='name2', code='code2')

    option_name = 'option'
    option2 = models.AttributeOption(group=option_group2, option=option_name)
    option2.save()

    with pytest.raises(django.core.validators.ValidationError):
        issue.attr.code = option2
        issue.clean()
