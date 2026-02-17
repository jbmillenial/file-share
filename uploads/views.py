from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import UploadedFile
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm

# from django.contrib.auth.models import User


def home(request):
    """
    Homepage - shows different content for logged in vs logged out users
    """
    context = {}

    if request.user.is_authenticated:
        # User is logged in - show their stats
        total_files = UploadedFile.objects.filter(user=request.user).count()
        active_files = UploadedFile.objects.filter(
            user=request.user
        ).exclude(
            expires_at__lt=timezone.now()
        ).count()

        total_size = sum(
            f.file_size for f in UploadedFile.objects.filter(user=request.user)
        )
        total_size_mb = round(total_size / (1024 * 1024), 2)

        context = {
            'total_files': total_files,
            'active_files': active_files,
            'total_size_mb': total_size_mb,
        }

    return render(request, 'uploads/home.html', context)


@login_required
def upload_file(request):
    """
    Handle file upload with validation
    """
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        expiry_days = request.POST.get('expiry_days', '')

        if not uploaded_file:
            messages.error(request, 'Please select a file to upload.')
            return render(request, 'uploads/upload.html')

        try:
            # Calculate expiry date
            expires_at = None
            if expiry_days and int(expiry_days) > 0:
                expires_at = timezone.now() + timedelta(days=int(expiry_days))

            # Save to database
            file_obj = UploadedFile.objects.create(
                user=request.user,
                original_filename=uploaded_file.name,
                file=uploaded_file,
                file_size=uploaded_file.size,
                expires_at=expires_at
            )

            messages.success(
                request,
                f'File "{uploaded_file.name}" uploaded successfully! '
                f'Size: {file_obj.size_in_mb()}MB'
            )
            return redirect('file_list')

        except ValidationError as e:
            # Validation failed
            messages.error(request, str(e.message))
        except Exception as e:
            # Other errors
            messages.error(request, f'Upload failed: {str(e)}')

    return render(request, 'uploads/upload.html')


@login_required
def file_list(request):
    """
    Show all files uploaded by this user
    """
    files = UploadedFile.objects.filter(user=request.user)

    # Separate active and expired files
    active_files = [f for f in files if not f.is_expired()]
    expired_files = [f for f in files if f.is_expired()]

    context = {
        'active_files': active_files,
        'expired_files': expired_files,
    }
    return render(request, 'uploads/file_list.html', context)


@login_required
def delete_file(request, file_id):
    """
    Delete a file
    """
    try:
        file_obj = UploadedFile.objects.get(id=file_id, user=request.user)
        filename = file_obj.original_filename

        # Delete from disk
        file_obj.file.delete()

        # Delete from database
        file_obj.delete()

        messages.success(request, f'File "{filename}" deleted successfully.')
    except UploadedFile.DoesNotExist:
        messages.error(request, 'File not found.')

    return redirect('file_list')


def register(request):
    """
    Handle user registration
    """
    if request.user.is_authenticated:
        # Already logged in, redirect to home
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()

            # Log them in automatically
            login(request, user)      
            messages.success(
                request, 
                f'Welcome {user.username}! Your account has been created.'
            )
            return redirect('home')
        else:
            # Form has errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show empty form
        form = UserRegistrationForm() 
    return render(request, 'uploads/register.html', {'form': form})


def logout_view(request):
    """
    Log out the user and redirect to home
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def shared_download(request, token):
    """
    Public download link - no login required
    Anyone with the token can download the file
    """
    try:
        file_obj = get_object_or_404(UploadedFile, share_token=token)

        # Check if file has expired
        if file_obj.is_expired():
            return render(request, 'uploads/link_expired.html', {
                'filename': file_obj.original_filename
            })

        # Serve the file
        response = FileResponse(file_obj.file.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{
            file_obj.original_filename
            }"'
        return response

    except Http404:
        return render(request, 'uploads/link_invalid.html')
