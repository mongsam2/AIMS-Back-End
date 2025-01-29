from django.contrib import admin
from .models import Document, DocumentType, RawData, Documentation


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'document_type', 'upload_date')


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ('file_url',)


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'document_type', 'file_url', 'state')