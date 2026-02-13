from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.customauth.urls')),
    path('api/v1/creators/', include('apps.creators.urls')),
    path('api/v1/wallets/', include('apps.wallets.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    # OpenAI Schema and Documentation
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/docs/', SpectacularRedocView.as_view(url_name='schema'), name='docs'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)