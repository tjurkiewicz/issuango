import django.shortcuts
import django.views.generic

import issuango.apps.user.mixins

import app
import forms


class CreateIssueView(issuango.apps.user.mixins.LoginRequiredMixin, django.views.generic.FormView):
    form_class = forms.CreateIssueForm
    template_name = 'issue/create.html'

    @property
    def projects(self):
        return self.request.user.roles

    def get(self, request, *args, **kwargs):
        if not self.projects.all():
            return django.shortcuts.redirect(app.application.reverse('no-projects'))
        return super(CreateIssueView, self).get(request, *args, **kwargs)


class NoProjectsView(issuango.apps.user.mixins.LoginRequiredMixin, django.views.generic.TemplateView):
    template_name = 'issue/no_projects.html'









