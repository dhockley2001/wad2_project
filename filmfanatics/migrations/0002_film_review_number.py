# Generated by Django 2.2.17 on 2021-03-24 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmfanatics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='review_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]