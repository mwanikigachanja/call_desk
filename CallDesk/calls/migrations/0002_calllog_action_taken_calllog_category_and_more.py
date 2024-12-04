# Generated by Django 5.1.1 on 2024-12-03 05:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calllog',
            name='action_taken',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='calllog',
            name='category',
            field=models.CharField(choices=[('Maize', 'Maize'), ('Wheat', 'Wheat'), ('Beans', 'Beans'), ('Fertilizers', 'Fertilizers'), ('Others', 'Others')], default='Others', max_length=50),
        ),
        migrations.AddField(
            model_name='calllog',
            name='recommendation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='calllog',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calls.customer'),
        ),
    ]