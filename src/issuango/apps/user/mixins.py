import django.contrib.auth.mixins
import django.core.urlresolvers

import app


class LoginRequiredMixin(django.contrib.auth.mixins.LoginRequiredMixin):
    login_url = django.core.urlresolvers.reverse_lazy('{0}:sign-in'.format(app.application.name))
