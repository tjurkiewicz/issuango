

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
