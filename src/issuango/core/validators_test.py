import keyword

import django.core.exceptions

import pytest

import validators


@pytest.mark.parametrize('kw', keyword.kwlist)
def test_python_keyword(kw):
    with pytest.raises(django.core.exceptions.ValidationError):
        validators.non_python_keyword(kw)


def test_non_python_keyword():
    assert 'klass' == validators.non_python_keyword('klass')
