# Generated by Django 5.0.7 on 2024-08-08 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_remove_shiped_address_order_id_orders_address_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='product_status',
            field=models.BooleanField(default=True),
        ),
    ]