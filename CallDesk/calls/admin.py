# calls/admin.py
from django.contrib import admin
from .models import Customer, CallLog

admin.site.register(Customer)
admin.site.register(CallLog)
