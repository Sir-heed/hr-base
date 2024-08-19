from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.choices import UserRole
from accounts.models import User
from accounts.serializers import UserSerializer
from core.serializers import ModelSerializer
from . import models


class OrganizationSerializer(ModelSerializer):
    class Meta(ModelSerializer.Meta):
        model = models.Organisation
        read_only_fields = [*ModelSerializer.Meta.read_only_fields, 'staff_access_code', 'admin']

    def before_validate(self, attrs):
        user = self.context['request'].user
        user.role = UserRole.ORG_ADMIN.value
        user.save()

        attrs['admin'] = user
        return super().before_validate(attrs)


class StaffSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=UserRole.USER.value),
    )
    role = serializers.ChoiceField(
        choices=[UserRole.ORG_HR.value, UserRole.ORG_STAFF.value],
        write_only=True,
    )

    class Meta(ModelSerializer.Meta):
        model = models.Staff
        read_only_fields = [*ModelSerializer.Meta.read_only_fields, 'organisation']

    def before_validate(self, attrs):
        admin = self.context['request'].user

        user = attrs['user']
        user.role = attrs.pop('role')
        user.save()

        attrs['organisation'] = admin.organisation

        return super().before_validate(attrs)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data

        return data


class StaffJoinSerializer(serializers.Serializer):
    org_access_code = serializers.CharField()

    def validate(self, attrs):
        org_access_code = attrs['org_access_code']
        user = self.context['request'].user

        if len(org_access_code) != 3:
            raise serializers.ValidationError({'org_access_code': _('Invalid code')})

        org = models.Organisation.objects.filter(staff_access_code=org_access_code).first()
        if not org:
            raise serializers.ValidationError(
                {'org_access_code': _('Organisation does not exist')},
            )
        
        if models.Staff.objects.filter(organisation=org, user=user).exists():
            raise serializers.ValidationError(
                {'error': _('You are a staff of the organisation already.')})

        attrs['org'] = org
        return super().validate(attrs)
