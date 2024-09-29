from django.urls import path
from .views import client_main_view

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('', client_main_view, name='client_main'),
    ]