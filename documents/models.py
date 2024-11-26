from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Make owner optional

    def __str__(self):
        return self.address

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('deed', 'Property Deed'),
        ('contract', 'Sales Contract'),
        ('inspection', 'Inspection Report'),
        ('other', 'Other'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='property_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Make uploaded_by optional
    file_size = models.IntegerField()
    mime_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.property.address}"

    class Meta:
        ordering = ['-uploaded_at']