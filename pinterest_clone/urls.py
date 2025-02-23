from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from images.views import image_upload, success_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('images.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

