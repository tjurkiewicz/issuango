import django.views.generic

import issuango.core.mixins


class IndexView(issuango.core.mixins.PermissionMixin, django.views.generic.TemplateView):
    template_name = 'dashboard/index.html'