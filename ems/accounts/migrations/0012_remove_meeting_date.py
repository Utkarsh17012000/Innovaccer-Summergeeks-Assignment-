# Generated by Django 2.2.8 on 2019-12-20 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20191218_0148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='date',
        ),
    ]
