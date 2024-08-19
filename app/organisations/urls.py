from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'organisations'

router = DefaultRouter()
router.register('', views.OrganisationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
