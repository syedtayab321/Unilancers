# Generated by Django 5.0.7 on 2024-08-13 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UniSeller', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gigdatamodal',
            name='gig_price',
        ),
    ]
