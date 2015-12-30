import django.apps
import django.utils.translation

_ = django.utils.translation.ugettext_lazy


class Dashboardonfig(django.apps.AppConfig):
    label = 'dashboard'
    name = 'issuango.apps.dashboard'
    verbose_name = _('Dashboard')
