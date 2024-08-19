from typing import Collection
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.choices import UserRole
from accounts.models import User
from core.models import BaseAbstractModel
from organisations.models import Organisation


class Job(BaseAbstractModel):
    title = models.CharField(max_length=250)
    description = models.TextField()
    org = models.ForeignKey(
        Organisation,
        related_name='jobs',
        on_delete=models.PROTECT,
    )
    created_by = models.ForeignKey(
        User,
        related_name='jobs_created',
        on_delete=models.PROTECT,
        limit_choices_to=models.Q(role=UserRole.ORG_HR.value)
    )
    updated_by = models.ForeignKey(
        User,
        related_name='jobs_updated',
        on_delete=models.PROTECT,
        limit_choices_to=models.Q(role=UserRole.ORG_HR.value)
    )

    class Meta(BaseAbstractModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['org', 'title'],
                condition=models.Q(is_active=True),
                name='unique_organisation_job_title',
                violation_error_message=_('Job already created.'),
            )
        ]


class Application(BaseAbstractModel):
    applicant = models.ForeignKey(
        User,
        related_name='applications',
        on_delete=models.PROTECT,
    )
    job = models.ForeignKey(
        Job,
        related_name='applications',
        on_delete=models.PROTECT,
    )
    skill_description = models.TextField()

    class Meta(BaseAbstractModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['applicant', 'job'],
                condition=models.Q(is_active=True),
                name='unique_job_applicant',
                violation_error_message=_('Application already created.'),
            )
        ]

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self._check_applicant()
        return super().clean()

    def _check_applicant(self):
        if self.job.org.staffs.filter(user=self.applicant).exists():
            raise ValidationError(
                {
                    'applicant': ValidationError(
                        _('You are already a staff of this job organisation.'),
                        code='invalid'
                    )
                }
            )
