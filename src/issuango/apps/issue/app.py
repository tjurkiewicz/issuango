import issuango.core.application

import views


class IssueApplication(issuango.core.application.Application):

    name = 'issue'

    views = [
        (views.IssueCreateView,      r'^issue/create/$',              'issue-create',       False,),
        (views.IssueCreateView,      r'^issue/(?P<slug>[-\w]+-\d+)$', 'issue-detail',       False,),

        (views.AttributeSchemeListView,   r'^attribute-scheme/$',        'attribute-scheme-list',   True,),
        (views.AttributeSchemeCreateView, r'^attribute-scheme/create/$', 'attribute-scheme-create', True,),
        (views.AttributeSchemeUpdateView, r'^attribute-scheme/update/(?P<code>[-\w]+)$', 'attribute-scheme-update', True,),
        (views.AttributeSchemeDeleteView, r'^attribute-scheme/delete/(?P<code>[-\w]+)$', 'attribute-scheme-delete', True,),

        (views.NoProjectsView,       r'^no-projects/$',               'no-projects',        False,),
    ]


application = IssueApplication()
