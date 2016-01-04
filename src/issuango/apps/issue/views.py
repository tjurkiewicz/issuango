import django.forms
import django.shortcuts
import django.views.generic

import issuango.core.mixins

import app
import forms
import models
import tables

class IssueCreateView(issuango.core.mixins.PermissionMixin, django.views.generic.CreateView):
    model = models.Issue
    form_class = forms.CreateIssueForm

    @property
    def projects(self):
        return self.request.user.roles

    def get(self, request, *args, **kwargs):
        if not self.projects.all():
            return django.shortcuts.redirect(app.application.reverse('no-projects'))
        return super(IssueCreateView, self).get(request, *args, **kwargs)


class IssueDetailView(issuango.core.mixins.PermissionMixin, django.views.generic.DetailView):
    model = models.Issue


class AttributeSchemeListView(issuango.core.mixins.PermissionMixin, django.views.generic.ListView):
    model = models.AttributeScheme

    def get_context_data(self, **kwargs):
        kwargs.update({
            'table': tables.AttributeSchemeTable(self.get_queryset().all()),
        })
        return super(AttributeSchemeListView, self).get_context_data(**kwargs)


class AttributeSchemeCreateView(issuango.core.mixins.PermissionMixin, django.views.generic.CreateView):
    model = models.AttributeScheme
    fields = ['name', 'code']

    def get_success_url(self):
        return app.application.reverse('attribute-scheme-list')


class AttributeSchemeUpdateView(issuango.core.mixins.PermissionMixin, django.views.generic.UpdateView):
    model = models.AttributeScheme
    fields = ['name', 'code']
    slug_field = slug_url_kwarg = 'code'

    def get_success_url(self):
        return app.application.reverse('attribute-scheme-list')


class AttributeSchemeDeleteView(issuango.core.mixins.PermissionMixin, django.views.generic.DeleteView):
    model = models.AttributeScheme
    fields = ['name', 'code']
    slug_field = slug_url_kwarg = 'code'

    def get_success_url(self):
        return app.application.reverse('attribute-scheme-list')



class NoProjectsView(issuango.core.mixins.PermissionMixin, django.views.generic.TemplateView):
    template_name = 'issue/no_projects.html'








