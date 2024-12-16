from django.db import models
from django.contrib.auth.models import AbstractUser, User, Category, ActionTaken

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class CallLog(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='call_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logged_calls')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='call_logs')
    description = models.TextField()
    action_taken = models.ForeignKey(ActionTaken, on_delete=models.SET_NULL, null=True, related_name='call_logs')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CallLog {self.id} - {self.customer.name}"


# Report Metadata Model (optional for future analytics)
class Report(models.Model):
    report_name = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Store metadata for analytics purposes

    def __str__(self):
        return self.report_name
    

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Agent', 'Agent'),
        ('Manager', 'Manager'),
        ('Supervisor', 'Supervisor'),
        ('Support', 'Support'),
        ('Analyst', 'Analyst'),
        ('Developer', 'Developer'),
        ('Tester', 'Tester'),
        ('Staff', 'Staff'),
        ('Other', 'Other'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Agent')

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class ActionTaken(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Recommendation(models.Model):
    call_log = models.ForeignKey('CallLog', on_delete=models.CASCADE, related_name='recommendations')
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.call_log.id}"

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ]
    report_name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_name



