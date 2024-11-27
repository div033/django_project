from rest_framework import serializers
from .models import Document, Property

class PropertySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = Property
        fields = ['id', 'address', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    download_url = serializers.SerializerMethodField()
    property = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        required=False,
        allow_null=True
    )

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