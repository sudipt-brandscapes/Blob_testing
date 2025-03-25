from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from .models import Document
from .forms import DocumentUploadForm
import os
from django.conf import settings
from django.core.exceptions import ValidationError

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        form = DocumentUploadForm(request.data, request.FILES)
        
        if not form.is_valid():
            return Response({
                'success': False,
                'message': 'Validation error',
                'errors': form.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            document = form.save()
            return Response({
                'success': True,
                'document': {
                    'id': document.id,
                    'title': document.title,
                    'uploaded_at': document.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        try:
            documents = Document.objects.all().order_by('-uploaded_at')
            documents_list = [{
                'id': doc.id,
                'title': doc.title,
                'file_url': doc.file.url,
                'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                'file_name': os.path.basename(doc.file.name)
            } for doc in documents]
            
            return Response({
                'success': True,
                'documents': documents_list
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentDownloadView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, document_id, format=None):
        try:
            document = Document.objects.get(id=document_id)
            # You can add download tracking or other logic here if needed
            return HttpResponseRedirect(document.file.url)
            
        except Document.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)