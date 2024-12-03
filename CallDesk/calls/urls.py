# calls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('call-log/', views.call_log, name='call_log'),
    path('customers/', views.customer_list, name='customer_list'),
    path('call-log/edit/<int:pk>/', views.edit_call_log, name='edit_call_log'),
    path('call-log/delete/<int:pk>/', views.delete_call_log, name='delete_call_log'),  # Delete URL
    path('call-log/assign/<int:pk>/', views.assign_call_log, name='assign_call_log'),  # Assign URL
     path('customers/edit/<int:pk>/', views.edit_customer, name='edit_customer'),  # Edit customer URL
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'), # Delete customer URL
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),  # Analytics page
]
