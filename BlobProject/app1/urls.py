from django.urls import path
from django.views.generic import TemplateView
from . import views
 
urlpatterns = [
    # API endpoints
    path('api/upload/', views.DocumentUploadView.as_view(), name='document-upload'),
    path('api/documents/', views.DocumentListView.as_view(), name='document-list'),
    path('api/documents/<int:document_id>/download/', views.DocumentDownloadView.as_view(), name='document-download'),
    # Serve React app at the root
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]