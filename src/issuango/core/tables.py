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
    """
        Allows the column to be rendered using selected template loader.

        Eg:

        import django.template.loader
        import django.util.translation
        import flask_table

        _ = django.util.translation.ugettext

        class DjangoTemplateCol(TemplateCol):
            loader = django.template.loader,get_template

        class MyTable(flask_table.Table):
            template_col = DjangoTemplateCol(_('My Template Column'), 'path/to/template.html')

    """

    template_loader = None

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


class DjangoTemplateCol(TemplateCol):
    pass


class SelectCol(flask_table.Col):

    def __init__(self, name='select_all', show=True):
        super(SelectCol, self).__init__(name, allow_sort=False, show=show)

    def _markup(self, **html_attrs):
        attrs = {
            'name': self.name,
            'type': 'checkbox',
        }

        attrs.update(html_attrs)
        html = ' '.join(map(lambda e: '{}="{}"'.format(*e), attrs.iteritems()))

        return flask.Markup(
            '<div class="checkbox">'
                '<label><input {}/> </label>'
            '</div>'.format(html))

    def th_contents(self, col_key):
        return self._markup(**{'data-item': ""})

    def td_contents(self, item, attr_list):
        return self._markup(**{'data-item': item.id})
