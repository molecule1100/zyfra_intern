from django.contrib.auth.mixins import UserPassesTestMixin


class GroupRequiredMixin(UserPassesTestMixin):
    allowed_groups = []

    def test_func(self):
        u = self.request.user
        if u.is_superuser:
            return True
        return u.groups.filter(name__in=self.allowed_groups).exists()
