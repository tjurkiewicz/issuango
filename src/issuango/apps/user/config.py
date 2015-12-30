import django.apps
import django.utils.translation

_ = django.utils.translation.ugettext_lazy


class UserConfig(django.apps.AppConfig):
    label = 'user'
    name = 'issuango.apps.user'
    verbose_name = _('User management')


