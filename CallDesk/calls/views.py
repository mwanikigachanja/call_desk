# calls/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer, CallLog
from .forms import CallLogForm, CustomerForm
from datetime import timedelta, datetime
from django.utils import timezone
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.signing import Signer
from django.urls import reverse
from django.db.models import Count, Avg, Q, F, DurationField, ExpressionWrapper

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
            messages.success(request, "Call log updated successfully.")
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

def get_analytics(start_date, end_date):
    total_queries = CallLog.objects.filter(created_at__range=[start_date, end_date]).count()
    resolved_queries = CallLog.objects.filter(
        created_at__range=[start_date, end_date], status='R'
    ).count()
    resolution_rate = (resolved_queries / total_queries) * 100 if total_queries > 0 else 0
    category_distribution = CallLog.objects.filter(
        created_at__range=[start_date, end_date]
    ).values('category').annotate(total=Count('id'))
    
    avg_resolution_time = CallLog.objects.filter(
        created_at__range=[start_date, end_date], status='R'
    ).aggregate(Avg('updated_at'))['updated_at__avg']  # Assuming you track resolution timestamps
    
    return {
        'total_queries': total_queries,
        'resolved_queries': resolved_queries,
        'resolution_rate': resolution_rate,
        'category_distribution': category_distribution,
        'avg_resolution_time': avg_resolution_time,
    }

def generate_pdf(context, template_path):
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None

def export_pdf(request):
    start_date = request.GET.get('start_date', datetime.now() - timedelta(days=30))
    end_date = request.GET.get('end_date', datetime.now())
    analytics = get_analytics(start_date, end_date)
    context = {'analytics': analytics}
    return generate_pdf(context, 'report_template.html')

def get_shareable_link(request, start_date, end_date):
    signer = Signer()
    signed_data = signer.sign(f"{start_date}:{end_date}")
    link = request.build_absolute_uri(
        reverse('report_view', args=[signed_data])
    )
    return link

def analytics_dashboard(request):
    # Metrics
    total_queries = CallLog.objects.count()
    open_queries = CallLog.objects.filter(status='Open').count()
    resolved_queries = CallLog.objects.filter(status='Resolved').count()

    # Average resolution time
    avg_resolution_time = CallLog.objects.filter(status='Resolved').aggregate(
        avg_time=Avg(ExpressionWrapper(F('updated_at') - F('created_at'), output_field=DurationField()))
    )['avg_time']

    # Queries by Status
    query_status_data = (
        CallLog.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )

    # Queries by Query Type
    query_type_data = (
        CallLog.objects.values('query_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Weekly Queries
    start_of_week = timezone.now() - timezone.timedelta(days=7)
    weekly_data = (
        CallLog.objects.filter(created_at__gte=start_of_week)
        .values('created_at__date')
        .annotate(count=Count('id'))
        .order_by('created_at__date')
    )

    context = {
        'total_queries': total_queries,
        'open_queries': open_queries,
        'resolved_queries': resolved_queries,
        'avg_resolution_time': avg_resolution_time,
        'query_status_data': query_status_data,
        'query_type_data': query_type_data,
        'weekly_data': weekly_data,
    }
    return render(request, 'analytics_dashboard.html', context)