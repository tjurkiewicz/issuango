import django.forms

import models


class CreateIssueForm(django.forms.ModelForm):
    class Meta:
        model = models.Issue
        fields = ['project']


