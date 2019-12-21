# Generated by Django 2.2.8 on 2019-12-13 18:10

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='enter name', max_length=256)),
                ('email', models.EmailField(help_text='enter email', max_length=254)),
                ('phone', phone_field.models.PhoneField(help_text='enter phone number', max_length=31)),
                ('account_type', models.CharField(max_length=7)),
            ],
        ),
    ]
