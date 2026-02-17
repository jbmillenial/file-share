from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('share/<str:token>/', views.shared_download, name='shared_download'),
]
