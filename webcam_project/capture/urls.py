# capture/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.capture_photo, name='capture_photo'),
    path('track/', views.face_tracking_view, name='face_tracking'),
    path('check-face/', views.face_check_view, name='face_check'),
]
