# Generated by Django 2.2.8 on 2019-12-17 19:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20191217_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 12, 17, 19, 32, 29, 810354, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
