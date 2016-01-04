import django.contrib.auth.mixins
import django.core.urlresolvers


class PermissionMixin(django.contrib.auth.mixins.UserPassesTestMixin):
    # This is a reasonable default for issue tracking system.
    login_required = True

    staff_required = False

    def get_login_url(self):
        import issuango.apps.user.app
        return issuango.apps.user.app.application.reverse('sign-in')

    def test_func(self):
        if self.login_required and not self.request.user.is_authenticated():
            return False

        if self.staff_required and not self.request.user.is_staff:
            return False

        return True


