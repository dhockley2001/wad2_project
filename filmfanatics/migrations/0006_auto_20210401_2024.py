# Generated by Django 2.2.17 on 2021-04-01 20:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('filmfanatics', '0005_auto_20210401_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='reset_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 1, 20, 24, 46, 726403, tzinfo=utc)),
        ),
    ]