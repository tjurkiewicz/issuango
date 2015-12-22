import django.views.generic

class IndexView(django.views.generic.TemplateView):
    template_name = 'dashboard/index.html'