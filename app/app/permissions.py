from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from accounts.choices import UserRole


class AppBasePermission(BasePermission):
    user_role = None
    message = _('You are not allowed to perform this action.')

    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != self.user_role:
            return False
        return True


class IsUser(AppBasePermission):
    user_role = UserRole.USER.value
    message = _('Only user are allowed to perform this action.')


class IsOrgAdmin(AppBasePermission):
    user_role = UserRole.ORG_ADMIN.value
    message = _('Only organisation admin are allowed to perform this action.')


class IsOrgStaff(AppBasePermission):
    user_role = UserRole.ORG_STAFF.value
    message = _('Only organisation staff are allowed to perform this action.')


class IsOrgHR(AppBasePermission):
    user_role = UserRole.ORG_HR.value
    message = _('Only organisation HR are allowed to perform this action.')
