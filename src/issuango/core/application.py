import six

import django.conf.urls
import django.core.urlresolvers
import django.utils.functional
import django.views.generic


class Application(object):

    name = None

    #views is list of view_specs: view_class, pattern, view_name, staff permission
    views = []

    def __init__(self, app_name=None):
        self.app_name = app_name

    def get_urls(self):
        spec_to_view = lambda view_class, pattern, name, staff: \
                           django.conf.urls.url(pattern, view_class.as_view(staff_required=staff), name=name)
        return [spec_to_view(*view_spec) for view_spec in self.views]

    @property
    # It will work like standard urls module.
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    def reverse(self, view_name, *args, **kwargs):
        view_name = '{0}:{1}'.format(self.name, view_name)
        return django.core.urlresolvers.reverse(view_name, *args, **kwargs)
