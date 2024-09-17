from django.urls import path
from .views import RegisterView, LoginView, UpdateDeviceIdView, SequenceDataView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-device-id/', UpdateDeviceIdView.as_view(), name='update_device_id'),
    path('sequence-data/', SequenceDataView.as_view(), name='sequence_data'),
]