# Generated by Django 4.2.11 on 2024-05-01 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('cancelled', 'cancelled')], default='pending', max_length=50),
        ),
    ]
