# Generated by Django 5.0 on 2024-02-25 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passengers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passengersaccount',
            old_name='nid',
            new_name='nid_no',
        ),
    ]
