import django.contrib.auth.mixins
import django.views.generic

import forms


class CreateIssueView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.FormView):
    form_class = forms.CreateIssueForm
    template_name = 'issue/create.html'








