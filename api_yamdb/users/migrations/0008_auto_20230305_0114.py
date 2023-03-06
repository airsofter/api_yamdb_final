# Generated by Django 3.2 on 2023-03-04 22:14

import django.core.validators
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[-a-zA-Z0-9_]+$', code='invalid_username', message='Поле не соответсвует требованиям.'), users.models.validate_username]),
        ),
    ]