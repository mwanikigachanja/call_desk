# Generated by Django 5.1.1 on 2024-12-02 05:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=100)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='CallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_type', models.CharField(choices=[('Complaint', 'Complaint'), ('Feedback', 'Feedback'), ('Query', 'Query')], max_length=50)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('IP', 'In Progress'), ('R', 'Resolved')], default='P', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_calls', to=settings.AUTH_USER_MODEL)),
                ('logged_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logged_calls', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_logs', to='calls.customer')),
            ],
        ),
    ]