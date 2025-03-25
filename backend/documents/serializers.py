from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'uploaded_at', 'file_url', 'file_name', 'file_size']

    def get_file_url(self, obj):
        return obj.file_url

    def get_file_name(self, obj):
        return obj.file_name

    def get_file_size(self, obj):
        return obj.file_size