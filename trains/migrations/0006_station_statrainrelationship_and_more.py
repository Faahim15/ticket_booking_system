# Generated by Django 5.0 on 2024-03-04 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0005_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='staTrainRelationship',
            field=models.ManyToManyField(to='trains.train'),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
