# Generated by Django 5.0 on 2024-03-14 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0023_train_ac_b_train_ac_s_train_f_seat_train_s_chair_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketbooking',
            name='choose_class',
            field=models.CharField(choices=[('AC_B', 'AC_B'), ('AC_S', 'AC_S'), ('SNIGDHA', 'SNIGDHA'), ('S_CHAIR', 'S_CHAIR'), ('SHULOV', 'SHULOV'), ('F_SEAT', 'F_SEAT')], default=''),
        ),
    ]