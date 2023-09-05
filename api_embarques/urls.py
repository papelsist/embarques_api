from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('applications.authentication.urls')),
    path('',include('applications.reportes.urls')),
    path('',include('applications.embarques.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
