import django.conf
import django.conf.urls
import django.conf.urls.static

import issuango.apps.dashboard.urls

urlpatterns = [
    django.conf.urls.url(r'^dashboard/', django.conf.urls.include(issuango.apps.dashboard.urls)),
] + django.conf.urls.static.static(django.conf.settings.STATIC_URL, document_root=django.conf.settings.STATIC_ROOT)
