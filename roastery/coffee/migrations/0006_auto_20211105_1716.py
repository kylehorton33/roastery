# Generated by Django 3.1.13 on 2021-11-05 17:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0005_auto_20211105_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roast',
            name='roast_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
