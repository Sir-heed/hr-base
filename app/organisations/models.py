from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import BaseAbstractModel, NamedAbstractModel
from accounts.models import User
from accounts.choices import UserRole
from . import generators


class Organisation(NamedAbstractModel):
    valuation = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.TextField(null=True, blank=True)
    admin = models.OneToOneField(
        User,
        related_name='organisation',
        on_delete=models.PROTECT,
        limit_choices_to=models.Q(role=UserRole.ORG_ADMIN.value),
    )
    staff_access_code = models.CharField(max_length=3, unique=True, default=generators.generate_staff_code)


class Staff(BaseAbstractModel):
    organisation = models.ForeignKey(Organisation, related_name='staffs', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        related_name='staffs',
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(role__in=[UserRole.ORG_STAFF.value, UserRole.ORG_HR.value]),
    )

    class Meta(BaseAbstractModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['organisation', 'user'],
                name='unique_organisation_staff',
                violation_error_message=_('User is already a staff of the organisation.'),
            )
        ]
