from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.serializers import ModelSerializer

from . import models


class JobSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = models.Job
        read_only_fields = [*ModelSerializer.Meta.read_only_fields, 'created_by', 'updated_by']
    
    def before_validate(self, attrs):
        user = self.context['request'].user

        attrs['updated_by'] = user

        if not self.instance:
            attrs['created_by'] = user

        return super().before_validate(attrs)

    def validate(self, attrs):
        user = self.context['request'].user
        org = attrs.get('org')

        if org and not org.staffs.filter(user=user).exists():
            raise serializers.ValidationError({'error': _('Invalid organisation.')})
        return super().validate(attrs)


class ApplicationSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = models.Application
        read_only_fields = [*ModelSerializer.Meta.read_only_fields, 'applicant', 'job']
    
    def before_validate(self, attrs):
        user = self.context['request'].user
        job = self.context['job']

        attrs['applicant'] = user
        attrs['job'] = job
        return super().before_validate(attrs)
