# Generated by Django 2.2.17 on 2021-04-01 18:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('filmfanatics', '0002_auto_20210401_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='picture',
            field=models.ImageField(blank=True, upload_to='media/profile_images/'),
        ),
        migrations.AlterField(
            model_name='film',
            name='reset_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 1, 18, 49, 44, 975332, tzinfo=utc)),
        ),
    ]
