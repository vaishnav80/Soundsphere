# Generated by Django 5.0.7 on 2024-08-04 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_shiped_address_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiped_address',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='shiped_address',
            name='pincode',
            field=models.CharField(verbose_name=6),
        ),
    ]
