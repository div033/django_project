import magic
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Document, Property
from .serializers import DocumentSerializer, PropertySerializer

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter documents by property and user
        property_id = self.request.query_params.get('property_id')
        if property_id:
            return Document.objects.filter(
                property_id=property_id,
                property__owner=self.request.user
            )
        return Document.objects.filter(property__owner=self.request.user)

    def perform_create(self, serializer):
        file_obj = self.request.FILES['file']
        # Get MIME type using python-magic
        mime_type = magic.from_buffer(file_obj.read(1024), mime=True)
        file_obj.seek(0)  # Reset file pointer

        serializer.save(
            uploaded_by=self.request.user,
            file_size=file_obj.size,
            mime_type=mime_type
        )

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        document = self.get_object()
        # Return pre-signed URL for temporary access
        return Response({
            'preview_url': document.file.url
        })

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        # Delete file from S3
        document.file.delete(save=False)
        return super().destroy(request, *args, **kwargs)

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)