# Generated by Django 3.1.13 on 2021-11-19 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0013_auto_20211117_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraction',
            name='time',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4, verbose_name='Time of Extraction [s]'),
            preserve_default=False,
        ),
    ]