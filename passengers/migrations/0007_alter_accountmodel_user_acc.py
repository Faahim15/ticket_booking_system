# Generated by Django 5.0 on 2024-03-10 11:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passengers', '0006_alter_accountmodel_user_acc'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountmodel',
            name='user_acc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deposit', to=settings.AUTH_USER_MODEL),
        ),
    ]
