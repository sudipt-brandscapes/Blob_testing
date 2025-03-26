from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from .models import Document

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        title = request.data.get('title')
        file = request.data.get('file')
        
        if not title or not file:
            return Response({
                'success': False,
                'message': 'Title and file are required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        document = Document.objects.create(
            title=title,
            file=file
        )
        
        return Response({
            'success': True,
            'document': {
                'id': document.id,
                'title': document.title,
                'file_url': document.file.url,
                'uploaded_at': document.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=status.HTTP_201_CREATED)

class DocumentListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        documents = Document.objects.all().order_by('-uploaded_at')
        documents_list = [{
            'id': doc.id,
            'title': doc.title,
            'file_url': doc.file.url,
            'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        } for doc in documents]
        
        return Response({
            'success': True,
            'documents': documents_list
        })

class DocumentDownloadView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, document_id, format=None):
        try:
            document = Document.objects.get(id=document_id)
            return HttpResponseRedirect(document.file.url)
        except Document.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)