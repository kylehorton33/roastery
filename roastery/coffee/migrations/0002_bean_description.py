# Generated by Django 3.1.13 on 2021-10-26 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bean',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description of Bean'),
        ),
    ]
