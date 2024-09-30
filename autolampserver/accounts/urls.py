from django.urls import path
from .views import RegisterView, LoginView, LogoutView, GetTokenView, GetUserView, UpdateDeviceIdView, SequenceDataView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-token/', GetTokenView.as_view(), name='get-token'),
    path('get-user/', GetUserView.as_view(), name='get-user'),
    path('update-device-id/', UpdateDeviceIdView.as_view(), name='update-device-id'),
    path('sequence-data/', SequenceDataView.as_view(), name='sequence-data'),
]