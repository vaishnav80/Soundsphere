# Generated by Django 5.0.7 on 2024-08-16 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_user_details_refferal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='refferal_code',
            field=models.CharField(blank=True, default='123456', max_length=10),
        ),
    ]
