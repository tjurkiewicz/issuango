import django.template
import django.template.loader

import flask
import flask_table


class BaseTable(flask_table.Table):
    classes = ['table', 'table-striped', 'table-hover']

    def th_contents(self, col_key, col):
        if isinstance(col, SelectCol):
            return col.th_contents(col_key)
        return super(BaseTable, self).th_contents(col_key, col)


class TemplateCol(flask_table.Col):

    def __init__(self, name, template_name, allow_sort=True, show=True):
        super(TemplateCol, self).__init__(name, allow_sort=allow_sort, show=show)
        self._template_name = template_name

    def td_contents(self, item, attr_list):
        template = django.template.loader.get_template(self._template_name)
        context = {
            'item': item,
            'attr_list': attr_list,
        }

        return template.render(context=context)


class SelectCol(flask_table.Col):

    def __init__(self, name, show=True):
        super(SelectCol, self).__init__(name, allow_sort=False, show=show)

    def th_contents(self, col_key):
        return flask.Markup('<div class="row-action-primary checkbox"><label><input type="checkbox"/></label></div>')

    def td_contents(self, item, attr_list):
        return flask.Markup('<div class="row-action-primary checkbox"><label><input type="checkbox"/></label></div>')
