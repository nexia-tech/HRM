
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users.admin import hrm_admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', hrm_admin.urls),
    path('',include('users.urls')),
    path('hrm/',include('hrm_app.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
