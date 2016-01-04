import django.views.generic.edit


class MultipleFormMixin(django.views.generic.edit.FormMixin):
    pass


class ProcessMultipleFormView(django.views.generic.edit.ProcessFormView):
    pass

