from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views


app_name = 'accounts'

router = DefaultRouter()
router.register('', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.CustomObtainTokenPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify-token'),
]
