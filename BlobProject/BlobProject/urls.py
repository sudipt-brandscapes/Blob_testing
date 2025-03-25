from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),  # Replace 'file_upload_app' with your actual app name
]
 
# Add these lines to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)