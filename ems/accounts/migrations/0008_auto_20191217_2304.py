# Generated by Django 2.2.8 on 2019-12-17 17:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_meeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 12, 17, 23, 4, 39, 571873)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='check_in_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='check_out_time',
            field=models.TimeField(),
        ),
    ]
