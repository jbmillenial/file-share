from django.core.exceptions import ValidationError
import os


def validate_file_size(file):
    # Limit file size to 10MB
    max_size_mb = 10
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert to bytes

    if file.size > max_size_bytes:
        file_size_mb = file.size / 1024 / 1024
        raise ValidationError(
            f'File size cannot exceed {max_size_mb}MB. '
            f'Your file is {file_size_mb:.2f}MB'
        )


def validate_file_extension(file):
    # Define allowed extensions
    allowed_extensions = [
        '.pdf',
        '.doc', '.docx',
        '.xls', '.xlsx',
        '.jpg', '.jpeg', '.png', '.gif',
        '.txt', '.csv',
        '.zip'
    ]

    # Get file extension
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(
            f'File type "{ext}" is not allowed. '
            f'Allowed types: {", ".join(allowed_extensions)}'
        )
