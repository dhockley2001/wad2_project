# Generated by Django 2.2.17 on 2021-03-30 19:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('filmfanatics', '0013_auto_20210330_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='reset_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 30, 19, 29, 15, 650540, tzinfo=utc)),
        ),
    ]
