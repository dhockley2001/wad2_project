# Generated by Django 2.2.17 on 2021-04-01 07:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('filmfanatics', '0002_auto_20210331_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='reset_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 1, 7, 35, 59, 88483, tzinfo=utc)),
        ),
    ]