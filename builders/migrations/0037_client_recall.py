# Generated by Django 4.1.7 on 2023-05-08 09:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('builders', '0036_alter_apartmentprice_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='recall',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
