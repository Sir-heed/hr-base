from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseAbstractModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        null=True,
        verbose_name=_('created'),
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
        null=True,
        verbose_name=_('modified on'),
    )

    class Meta:
        abstract = True
        ordering = ("-created",)


class NamedAbstractModel(BaseAbstractModel):
    name = models.TextField(verbose_name=_('name'))

    class Meta(BaseAbstractModel.Meta):
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(is_active=True),
                name='unique_%(app_label)s_%(class)s_name',
                violation_error_message=_('Record with this name already exists'),
                violation_error_code='duplicated',
            ),
        ]
    
    def __str__(self):
        return self.name
