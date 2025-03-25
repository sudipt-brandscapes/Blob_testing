import logging
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
from storages.backends.azure_storage import AzureStorage

logger = logging.getLogger(__name__)

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        form = DocumentUploadForm(request.data, request.FILES)
        
        if not form.is_valid():
            logger.warning(f"Form validation failed: {form.errors}")
            return Response({
                'success': False,
                'message': 'Validation error',
                'errors': form.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            document = form.save()
            
            # Verify file was saved to Azure
            storage = AzureStorage()
            if not storage.exists(document.file.name):
                raise Exception("File was not properly saved to Azure Blob Storage")
            
            logger.info(f"Document uploaded successfully: {document.title}")
            return Response({
                'success': True,
                'document': {
                    'id': document.id,
                    'title': document.title,
                    'uploaded_at': document.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'file_url': document.file.url,
                    'file_name': os.path.basename(document.file.name),
                    'file_size': document.file.size
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            return Response({
                'success': False,
                'message': 'Failed to upload document to Azure Blob Storage'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        try:
            documents = Document.objects.all().order_by('-uploaded_at')
            
            # Test Azure connection
            storage = AzureStorage()
            if not storage.exists(''):  # Test listing
                raise Exception("Cannot connect to Azure Blob Storage")
            
            documents_list = []
            for doc in documents:
                try:
                    documents_list.append({
                        'id': doc.id,
                        'title': doc.title,
                        'file_url': doc.file.url,
                        'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'file_name': os.path.basename(doc.file.name),
                        'file_size': doc.file.size,
                        'file_type': os.path.splitext(doc.file.name)[1].lower()
                    })
                except Exception as e:
                    logger.error(f"Error processing document {doc.id}: {str(e)}")
                    continue
            
            return Response({
                'success': True,
                'documents': documents_list
            })
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return Response({
                'success': False,
                'message': 'Failed to retrieve documents from Azure Blob Storage'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentDownloadView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, document_id, format=None):
        try:
            document = Document.objects.get(id=document_id)
            
            # Verify file exists in Azure
            storage = AzureStorage()
            if not storage.exists(document.file.name):
                raise Exception("File not found in Azure Blob Storage")
            
            # Force download with original filename
            response = HttpResponseRedirect(document.file.url)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document.file.name)}"'
            return response
            
        except Document.DoesNotExist:
            logger.warning(f"Document not found: {document_id}")
            return Response({
                'success': False,
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Error downloading document {document_id}: {str(e)}")
            return Response({
                'success': False,
                'message': 'Failed to download document from Azure Blob Storage'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)