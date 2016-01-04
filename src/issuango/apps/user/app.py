import issuango.core.application

import views


class UserManagementApplication(issuango.core.application.Application):

    name = 'user'

    views = [
        (views.SignInView,  r'^sign-in/$',  'sign-in',  False),
        (views.SignOutView, r'^sign-out/$', 'sign-out', False),
    ]

application = UserManagementApplication()
