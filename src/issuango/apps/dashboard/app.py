import django.conf.urls

import issuango.core.application

import views


class DashboardApplication(issuango.core.application.Application):
    name = 'dashboard'

    index_view = views.IndexView

    def get_urls(self):
        return [
            django.conf.urls.url(r'$', self.index_view.as_view(), name='index'),
        ]

application = DashboardApplication()
