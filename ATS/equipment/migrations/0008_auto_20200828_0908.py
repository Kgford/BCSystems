# Generated by Django 3.0.8 on 2020-08-28 13:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0007_auto_20200828_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='last_update',
            field=models.DateField(default=datetime.datetime(2020, 8, 28, 9, 8, 45, 168470)),
        ),
    ]
