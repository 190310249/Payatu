from django.urls import path, include
from django.conf import settings
from firmware_manager.views import *

urlpatterns = [
    path('upload-firmware/', FirmwareCreateView.as_view(), name='upload-firmware'),
    path('firmware_by_user/<str:user_id>/', UserFirmwareListView.as_view(), name='user-firmware-list'),
    path('firmware_details/<str:uuid>/', UserFirmwareDetailView.as_view(), name='firmware-detail'),
]
