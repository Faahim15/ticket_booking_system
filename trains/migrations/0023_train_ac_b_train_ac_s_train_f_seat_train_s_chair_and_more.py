# Generated by Django 5.0 on 2024-03-14 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0022_alter_train_station_name_alter_train_ticket_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='ac_b',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='train',
            name='ac_s',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='train',
            name='f_seat',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='train',
            name='s_chair',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='train',
            name='snigdha',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
