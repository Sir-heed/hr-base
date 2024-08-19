from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'jobs'

router = DefaultRouter()
router.register('', views.JobViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
