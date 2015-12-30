import django.conf.urls

import issuango.core.application

import views


class UserManagementApplication(issuango.core.application.Application):
    name = 'user'

    sign_in_view = views.SignInView
    sign_out_view = views.SignOutView

    def get_urls(self):
        return [
            django.conf.urls.url(r'^sign-in/$', self.sign_in_view.as_view(), name='sign-in'),
            django.conf.urls.url(r'^sign-out/$', self.sign_out_view.as_view(), name='sign-out'),
        ]

application = UserManagementApplication()
