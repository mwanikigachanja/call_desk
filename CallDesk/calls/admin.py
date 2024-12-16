# calls/admin.py
from django.contrib import admin
from .models import Customer, User, Category, ActionTaken, Recommendation, CallLog, Report

admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(ActionTaken)
admin.site.register(Recommendation)
admin.site.register(CallLog)
admin.site.register(Report)
