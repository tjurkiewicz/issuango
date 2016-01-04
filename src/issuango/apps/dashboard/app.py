import issuango.core.application

import views


class DashboardApplication(issuango.core.application.Application):

    name = 'dashboard'

    views = [
        (views.IndexView, r'$', 'index', False),
    ]

application = DashboardApplication()
