from django.conf.urls.static import static
from django.contrib import admin
from . import settings
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('Main.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)