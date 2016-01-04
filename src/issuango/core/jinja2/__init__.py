import django.conf
import django.contrib.staticfiles.storage
import django.core.urlresolvers
import django.utils.timezone

import jinja2
import widget_tweaks.templatetags.widget_tweaks

import extras


def append_once(list, element):
    if element not in list:
        list.append(element)


def environment(**opts):
    extensions = opts.get('extensions', [])
    append_once(extensions, 'jinja2.ext.i18n')
    append_once(extensions, 'jinja2.ext.with_')
    opts['extensions'] = extensions

    env = jinja2.Environment(**opts)
    env.globals.update({
        'field_type': extras.field_type,
        'strftime': extras.strftime,

        'render_with_class': widget_tweaks.templatetags.widget_tweaks.add_class,


        'settings': django.conf.settings,
        'static': django.contrib.staticfiles.storage.staticfiles_storage.url,
        'url': django.core.urlresolvers.reverse
    })
    env.install_null_translations()

    print opts, env
    return env
