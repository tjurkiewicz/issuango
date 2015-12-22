import keyword

import django.core.exceptions
import django.utils.translation

_ = django.utils.translation.ugettext_lazy


def non_python_keyword(value):
    if keyword.iskeyword(value):
        raise django.core.exceptionsValidationError(_("This field is invalid as its value is forbidden"))
    return value
