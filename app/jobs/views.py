from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app import permissions
from app.utils import PaginatorMixin
from accounts.choices import UserRole
from . import models, serializers


class JobViewSet(PaginatorMixin, ListModelMixin, GenericViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer

    def org_qs(self):
        q = Q()

        user = self.request.user
        if user.role == UserRole.ORG_ADMIN.value:
            q &= Q(org=user.organisation)
        
        elif user.role in [UserRole.ORG_HR.value, UserRole.ORG_STAFF.value]:
            user_orgs = user.staffs.values_list('organisation__id')
            q &= Q(org__in=user_orgs)
        
        return self.get_queryset().filter(q)

    @action(
        detail=False,
        methods=['POST'],
        url_path='create',
        permission_classes=[permissions.IsOrgHR],
    )
    def create_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(
        detail=True,
        methods=['PATCH'],
        url_path='update',
        permission_classes=[permissions.IsOrgHR],
    )
    def update_job(self, request, pk=None):
        obj = get_object_or_404(self.org_qs(), pk=pk)

        serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(
        detail=True,
        methods=['POST'],
        url_path='apply',
        permission_classes=[IsAuthenticated],
        serializer_class=serializers.ApplicationSerializer,
    )
    def job_apply(self, request, pk=None):
        job = self.get_object()

        context = self.get_serializer_context()
        serializer = self.get_serializer(data=request.data, context={**context, 'job': job})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(
        detail=True,
        methods=['GET'],
        url_path='applications',
        permission_classes=[permissions.IsOrgHR | permissions.IsOrgAdmin],
        serializer_class=serializers.ApplicationSerializer,
    )
    def applications(self, request, pk=None):
        job = get_object_or_404(self.org_qs(), pk=pk)
        applications = job.applications.all()
        return self.paginate_results(applications)
