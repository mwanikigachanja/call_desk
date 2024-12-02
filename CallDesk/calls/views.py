# calls/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer, CallLog
from .forms import CallLogForm, CustomerForm

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

def edit_call_log(request, pk):
    call_log = get_object_or_404(CallLog, pk=pk)
    if request.method == "POST":
        form = CallLogForm(request.POST, instance=call_log)
        if form.is_valid():
            form.save()
            return redirect('call_log')
    else:
        form = CallLogForm(instance=call_log)
    return render(request, 'edit_call_log.html', {'form': form})

def delete_call_log(request, pk):
    call_log = get_object_or_404(CallLog, pk=pk)
    call_log.delete()
    messages.success(request, "Call log deleted successfully.")
    return redirect('call_log')

def assign_call_log(request, pk):
    call_log = get_object_or_404(CallLog, pk=pk)
    if request.method == "POST":
        user_id = request.POST.get('assigned_to')
        assigned_user = get_object_or_404(User, pk=user_id)
        call_log.assigned_to = assigned_user
        call_log.save()
        messages.success(request, f"Call log assigned to {assigned_user.username}.")
        return redirect('call_log')

    # Fetch all users to display in the dropdown
    users = User.objects.all()
    return render(request, 'assign_call_log.html', {'call_log': call_log, 'users': users})

def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated successfully.")
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})

def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, "Customer deleted successfully.")
    return redirect('customer_list')