import django.conf
import django.conf.urls
import django.conf.urls.static

import issuango.apps.dashboard.urls
import issuango.apps.issue.app

urlpatterns = [
    django.conf.urls.url(r'^dashboard/', django.conf.urls.include(issuango.apps.dashboard.urls)),
    django.conf.urls.url(r'^issues/', django.conf.urls.include(issuango.apps.issue.app.application.urls)),

] + django.conf.urls.static.static(django.conf.settings.STATIC_URL, document_root=django.conf.settings.STATIC_ROOT)
