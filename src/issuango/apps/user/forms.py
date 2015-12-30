import django.contrib.auth.forms as auth_forms
import django.forms
import django.utils.translation

_ = django.utils.translation.ugettext


class SignInForm(auth_forms.AuthenticationForm):
    remember = django.forms.BooleanField(label=_('Remember me'), required=False)

