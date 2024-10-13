from django.urls import path
from .views import client_main_view, client_conv_view

urlpatterns = [
    path('', client_main_view, name='client_main'),
    path('conv/', client_conv_view, name="client_conv"),
    ]