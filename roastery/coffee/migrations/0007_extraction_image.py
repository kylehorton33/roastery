# Generated by Django 3.1.13 on 2021-11-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0006_auto_20211105_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraction',
            name='image',
            field=models.ImageField(null=True, upload_to='extraction/'),
        ),
    ]