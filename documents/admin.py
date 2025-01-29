from django.contrib import admin
from .models import Document, DocumentType, RawData


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'document_type', 'upload_date')


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ('file_url',)