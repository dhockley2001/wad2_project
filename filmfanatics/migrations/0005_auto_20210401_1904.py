# Generated by Django 2.2.17 on 2021-04-01 19:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('filmfanatics', '0004_auto_20210401_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='reset_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 1, 19, 4, 46, 550422, tzinfo=utc)),
        ),
    ]
