from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from . import models, serializers


class CustomObtainTokenPairView(TokenObtainPairView):
    serializer_class = serializers.CustomObtainTokenPairSerializer


class UserViewSet(GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(
        detail=False,
        methods=['POST'],
        url_path='create',
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def create_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(
        detail=False,
        methods=['GET'],
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        return Response(status=status.HTTP_200_OK, data=self.get_serializer(request.user).data)
