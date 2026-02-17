# Django File Upload & Share App

A secure cloud-based file upload and sharing application built with Django and AWS S3.

## Features

- **User Authentication**: Register, login, and manage your account
- **File Upload**: Upload files with validation (10MB limit, multiple formats)
- **File Expiration**: Set automatic deletion after 1, 7, 30, or 90 days
- **Shareable Links**: Generate unique, shareable download links
- **Cloud Storage**: Files stored securely in AWS S3
- **Dashboard**: Track your uploads, storage usage, and file stats

## Tech Stack

- **Backend**: Django 5.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Storage**: AWS S3
- **Deployment**: AWS EC2
- **Server**: Gunicorn + Nginx

## Local Development Setup

### Prerequisites
- Python 3.10+
- pip
- virtualenv

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <project-folder>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Update `.env` with your settings:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_S3=False
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create superuser:
```bash
python manage.py createsuperuser
```

8. Run development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000`

## AWS Deployment

### Prerequisites
- AWS Account
- AWS CLI configured
- S3 Bucket created
- EC2 instance running

### Environment Variables for Production

Update `.env` on your EC2 instance:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

### Deployment Steps
(Detailed steps will be added during deployment)

## Project Structure

```
project/
├── core/                  # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── uploads/               # Main app
│   ├── models.py         # File upload models
│   ├── views.py          # Application views
│   ├── forms.py          # User registration forms
│   ├── templates/        # HTML templates
│   └── validators.py     # File validation
├── media/                # Local file storage (dev)
├── staticfiles/          # Collected static files
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
├── .env.example          # Environment template
└── .gitignore           # Git ignore rules
```

## File Size & Type Limits

- **Max file size**: 10MB
- **Allowed types**: PDF, Word, Excel, Images (JPG, PNG, GIF), TXT, CSV, ZIP

## Security Features

- User authentication required for uploads
- Unique, unguessable share tokens (UUID)
- File expiration dates
- CSRF protection
- Secure password hashing
- AWS IAM policies for S3 access

## Contributing

This is a portfolio project. Suggestions and feedback are welcome!

## License

MIT License - Feel free to use for learning purposes

## Author

Mathew Babdang Joseph - https://mathewbjoseph.com

## Acknowledgments

- Built as an AWS deployment portfolio project
- Demonstrates Django + AWS integration