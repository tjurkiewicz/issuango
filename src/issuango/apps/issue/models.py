import django.conf
import django.db.models


User = django.conf.settings.AUTH_USER_MODEL


class Issue(django.db.models.Model):
    key      = django.db.models.SlugField()
    assignee = django.db.models.ForeignKey(User, null=True, blank=True)
    reporter = django.db.models.ForeignKey(User)

    description = django.db.models.TextField()

    created = django.db.models.DateTimeField(auto_now_add=True)
    updated = django.db.models.DateTimeField(auto_now=True)

