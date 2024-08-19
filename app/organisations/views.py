from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from accounts.choices import UserRole
from core import permissions
from core.utils import PaginatorMixin
from . import models, serializers


class OrganisationViewSet(PaginatorMixin, ListModelMixin, GenericViewSet):
    queryset = models.Organisation.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = [permissions.IsOrgAdmin]

    def get_queryset(self):
        return super().get_queryset().filter(admin=self.request.user)

    @transaction.atomic
    @action(
        detail=False,
        methods=['POST'],
        url_path='create',
        permission_classes=[permissions.IsUser],
    )
    def create_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @transaction.atomic
    @action(
        detail=False,
        methods=['GET', 'POST'],
        url_path='staff',
        permission_classes=[permissions.IsOrgAdmin],
        serializer_class=serializers.StaffSerializer,
    )
    def staff(self, request):
        if request.method == 'GET':
            qs = (
                models.Staff
                .objects
                .filter(organisation__admin=request.user)
                .select_related('user').all()
            )
            return self.paginate_results(qs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(
        detail=False,
        methods=['POST'],
        url_path='staff/join',
        permission_classes=[permissions.IsUser],
        serializer_class=serializers.StaffJoinSerializer,
    )
    def staff_join(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.role = UserRole.ORG_STAFF.value
        user.save()

        models.Staff.objects.create(
            user=request.user,
            organisation=serializer.validated_data['org'],
        )

        return Response(
            status=status.HTTP_200_OK,
            data={'message': 'Joined organisation successfully.'},
        )
