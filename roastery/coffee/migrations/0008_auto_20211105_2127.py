# Generated by Django 3.1.13 on 2021-11-05 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0007_extraction_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraction',
            name='method',
            field=models.CharField(choices=[('espresso', 'Espresso'), ('v60', 'V60'), ('chemex', 'Chemex'), ('french-press', 'French Press')], default='espresso', max_length=20, verbose_name='Method of Extraction'),
        ),
    ]