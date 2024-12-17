from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


# Customer model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add a default
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # Customize the reverse accessor names to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="calls_user_groups",
        related_query_name="calls_user_group",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="calls_user_permissions",
        related_query_name="calls_user_permission",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

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
    
class CallLog(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    QUERY_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Feedback', 'Feedback'),
        ('Query', 'Query'),
    ]

    CATEGORY_CHOICES = [
        ('Maize', 'Maize'),
        ('Wheat', 'Wheat'),
        ('Beans', 'Beans'),
        ('Fertilizers', 'Fertilizers'),
        ('Others', 'Others'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='call_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logged_calls')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='call_logs')
    query_type = models.CharField(max_length=50, choices=QUERY_CHOICES)  # Add this field
    description = models.TextField()
    action_taken = models.ForeignKey(ActionTaken, on_delete=models.SET_NULL, null=True, related_name='call_logs')
    recommendation = models.TextField(blank=True, null=True)  # Add this field
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CallLog {self.id} - {self.customer.name}"

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
    




