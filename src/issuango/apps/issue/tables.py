import django.utils.http
import django.utils.translation

import flask_table

import issuango.core.tables

import app


_ = django.utils.translation.ugettext


class AttributeSchemeTable(issuango.core.tables.BaseTable):
    allow_sort = True

    select_all = issuango.core.tables.SelectCol(_('Select all'))
    name = flask_table.Col(_('Name'))
    code = flask_table.Col(_('Code'))
    edit = issuango.core.tables.TemplateCol(_('Actions'), 'issue/attributescheme_list_actions.html', allow_sort=False)

    def sort_url(self, col_key, reverse=False):
        kwargs = {
            'o': reverse and 'desc' or 'asc',
            'k': col_key,
        }

        return '{}?{}'.format(app.application.reverse('attribute-scheme-list'), django.utils.http.urlencode(kwargs))

