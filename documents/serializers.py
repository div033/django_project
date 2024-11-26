from rest_framework import serializers
from .models import Document, Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'address', 'created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'property', 'title', 'document_type', 'file', 
                 'uploaded_at', 'updated_at', 'file_size', 'mime_type', 
                 'download_url']
        read_only_fields = ['file_size', 'mime_type', 'download_url']

    def get_download_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url)
        return None