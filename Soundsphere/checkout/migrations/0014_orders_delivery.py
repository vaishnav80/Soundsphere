# Generated by Django 5.0.7 on 2024-08-24 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0013_alter_orders_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivery',
            field=models.IntegerField(default=0),
        ),
    ]
