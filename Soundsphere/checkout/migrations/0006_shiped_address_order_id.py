# Generated by Django 5.0.7 on 2024-08-04 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_shiped_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiped_address',
            name='order_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='checkout.orders'),
        ),
    ]