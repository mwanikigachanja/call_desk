# calls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('call-log/', views.call_log, name='call_log'),
    path('customers/', views.customer_list, name='customer_list'),
]
