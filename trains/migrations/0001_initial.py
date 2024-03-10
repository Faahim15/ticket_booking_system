# Generated by Django 5.0 on 2024-02-26 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_number', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('departure_time', models.DateTimeField(auto_now_add=True)),
                ('arrival_time', models.TimeField()),
                ('total_seats', models.PositiveIntegerField()),
                ('available_seats', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['departure_time'],
            },
        ),
    ]
