from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/v1/doc/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('org/', include('organisations.urls')),
    path('jobs/', include('jobs.urls'))
]
