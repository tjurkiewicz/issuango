import django.conf.urls

import issuango.core.application

import views


class IssueApplication(issuango.core.application.Application):
    name = 'issue'

    create_issue_view = views.CreateIssueView
    no_projects_view = views.NoProjectsView

    def get_urls(self):
        return [
            django.conf.urls.url(r'^create/$', self.create_issue_view.as_view(), name='create'),
            django.conf.urls.url(r'^no-projects/$', self.no_projects_view.as_view(), name='no-projects'),
        ]

application = IssueApplication()
