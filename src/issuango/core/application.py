import django.core.urlresolvers


class Application(object):

    name = None

    def __init__(self, app_name=None):
        self.app_name = app_name

    def get_urls(self):
        return []

    @property
    # It will work like standard urls module.
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    def reverse(self, view_name, *args, **kwargs):
        view_name = '{0}:{1}'.format(self.name, view_name)
        return django.core.urlresolvers.reverse(view_name, *args, **kwargs)