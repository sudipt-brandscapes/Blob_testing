from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document
from .serializers import DocumentSerializer

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
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
        
        serializer = DocumentSerializer(document)
        return Response({
            'success': True,
            'document': serializer.data
        }, status=status.HTTP_201_CREATED)

class DocumentListView(APIView):
    def get(self, request, format=None):
        documents = Document.objects.all().order_by('-uploaded_at')
        serializer = DocumentSerializer(documents, many=True)
        return Response({
            'success': True,
            'documents': serializer.data
        })

class DocumentDownloadView(APIView):
    def get(self, request, document_id, format=None):
        try:
            document = Document.objects.get(id=document_id)
            return Response({
                'success': True,
                'file_url': document.file_url
            })
        except Document.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)