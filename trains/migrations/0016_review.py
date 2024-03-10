# Generated by Django 5.0 on 2024-03-10 10:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0015_remove_train_statrainrelationship_train_station_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='trains.train')),
                ('user_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
