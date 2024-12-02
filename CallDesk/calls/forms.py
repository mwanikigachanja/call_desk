from django import forms
from .models import CallLog

class CallLogForm(forms.ModelForm):
    class Meta:
        model = CallLog
        fields = ['customer', 'query_type', 'description', 'status', 'assigned_to']
