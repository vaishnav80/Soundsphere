# Generated by Django 5.0.7 on 2024-08-11 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_items_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orders',
            name='total',
            field=models.IntegerField(default=999),
        ),
    ]