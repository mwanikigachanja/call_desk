# calls/models.py
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    query_type = models.CharField(max_length=50, choices=QUERY_CHOICES)
    description = models.TextField()
    logged_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logged_calls')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_calls', blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.query_type}"
