import django.core.exceptions

import pytest

import validators


def test_python_keyword():
    with pytest.raises(django.core.exceptions.ValidationError):
        validators.non_python_keyword('class')


def test_non_python_keyword():
    assert 'klass' == validators.non_python_keyword('klass')
