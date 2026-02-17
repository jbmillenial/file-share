from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'user', 'uploaded_at')
    search_fields = ('original_filename', 'user__username')
    list_filter = ('uploaded_at',)
