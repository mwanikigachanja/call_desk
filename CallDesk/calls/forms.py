from django import forms
from .models import CallLog, Customer

class CallLogForm(forms.ModelForm):
    class Meta:
        model = CallLog
        fields = ['customer', 'query_type', 'category', 'description', 'action_taken', 'recommendation', 'status', 'assigned_to']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
