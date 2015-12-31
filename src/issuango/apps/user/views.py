import django.conf
import django.contrib.auth
import django.core.urlresolvers
import django.shortcuts
import django.views.generic

import forms

import issuango.apps.dashboard.app


class SignInView(django.views.generic.FormView):
    form_class = forms.SignInForm
    template_name = 'user/login.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return django.shortcuts.redirect(django.conf.settings.LOGIN_REDIRECT_URL)
        return super(SignInView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get(self.redirect_field_name, '')

    def form_valid(self, form):
        django.contrib.auth.login(self.request, form.get_user())
        return super(SignInView, self).form_valid(form)


class SignOutView(django.views.generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        django.contrib.auth.logout(self.request)
        return issuango.apps.dashboard.app.application.reverse('index')

