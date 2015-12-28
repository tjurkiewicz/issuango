import django.apps
import django.utils.translation

_ = django.utils.translation.ugettext_lazy


class IssueConfig(django.apps.AppConfig):
    label = 'issue'
    name = 'issuango.apps.issue'
    verbose_name = _('Issues')


