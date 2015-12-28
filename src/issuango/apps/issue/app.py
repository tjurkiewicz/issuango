import django.conf.urls

import issuango.core.application

import views


class IssueApplication(issuango.core.application.Application):
    name = 'issue'

    create_issue_view = views.CreateIssueView

    def get_urls(self):
        return [
            django.conf.urls.url(r'^create/$', self.create_issue_view.as_view(), name='create'),
        ]

application = IssueApplication()
