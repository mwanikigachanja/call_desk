from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# CallLog Model
class CallLog(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('IP', 'In Progress'),
        ('R', 'Resolved'),
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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    query_type = models.CharField(max_length=50, choices=QUERY_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Others')  # New field
    description = models.TextField()
    action_taken = models.TextField(blank=True, null=True)  # New field
    recommendation = models.TextField(blank=True, null=True)  # New field
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logged_calls')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_calls', blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.query_type}"



# Report Metadata Model (optional for future analytics)
class Report(models.Model):
    report_name = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Store metadata for analytics purposes

    def __str__(self):
        return self.report_name
