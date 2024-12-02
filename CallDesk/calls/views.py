# calls/views.py
from django.shortcuts import render
from .models import Customer, CallLog

def dashboard(request):
    stats = {
        'total_queries': CallLog.objects.count(),
        'open_queries': CallLog.objects.filter(status='P').count(),
        'resolved_queries': CallLog.objects.filter(status='R').count(),
    }
    return render(request, 'dashboard.html', {'stats': stats})

def call_log(request):
    calls = CallLog.objects.all().order_by('-created_at')
    return render(request, 'call_log.html', {'calls': calls})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})
