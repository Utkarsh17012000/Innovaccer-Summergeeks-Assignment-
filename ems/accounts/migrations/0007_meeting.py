# Generated by Django 2.2.8 on 2019-12-16 19:25

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_account_fk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_name', models.CharField(max_length=256)),
                ('visitor_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('host_id', models.CharField(max_length=500)),
                ('check_in_time', models.DateTimeField()),
                ('check_out_time', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=1000)),
            ],
        ),
    ]
