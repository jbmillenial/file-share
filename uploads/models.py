from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from datetime import timedelta
from django.core.exceptions import ValidationError
import uuid
from .validators import validate_file_size, validate_file_extension


class UploadedFile(models.Model):
    """
    Represents a file uploaded by a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='uploads/',
        validators=[validate_file_size, validate_file_extension]
    )
    file_size = models.IntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    share_token = models.CharField(max_length=64, unique=True, blank=True)

    MAX_FILE_SIZE = 100 * 1024 * 1024

    def save(self, *args, **kwargs):
        # Validate file size
        if self.file_size > self.MAX_FILE_SIZE:
            raise ValidationError(
                f'File size exceeds maximum allowed size of '
                f'{self.MAX_FILE_SIZE / (1024*1024)}MB'
            )

        # Generate share token if it doesn't exist
        if not self.share_token:
            self.share_token = self.generate_share_token()

        super().save(*args, **kwargs)

    def generate_share_token(self):
        """Generate a unique shareable token"""
        return str(uuid.uuid4())

    def is_expired(self):
        # Check if file has expired
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False

    def size_in_mb(self):
        # Return file size in MB for display
        return round(self.file_size / (1024 * 1024), 2)

    def get_share_url(self):
        """Get the full shareable URL (add domain in production)"""
        from django.urls import reverse
        return reverse('shared_download', kwargs={'token': self.share_token})

    def __str__(self):
        return f"{self.original_filename} - {self.user.username}"

    class Meta:
        ordering = ['-uploaded_at']
