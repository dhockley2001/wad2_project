# Generated by Django 2.2.17 on 2021-04-01 14:54

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('director', models.CharField(max_length=30)),
                ('cast', models.TextField()),
                ('picture', models.ImageField(upload_to='film_images')),
                ('synopsis', models.TextField()),
                ('release', models.DateField(null=True)),
                ('views', models.IntegerField(default=0)),
                ('reset_at', models.DateTimeField(default=datetime.datetime(2021, 4, 1, 14, 54, 14, 96664, tzinfo=utc))),
                ('average_rating', models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('review_number', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('graphic', models.ImageField(upload_to='genre_graphics')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmfanatics.Account')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmfanatics.Film')),
            ],
        ),
        migrations.AddField(
            model_name='film',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmfanatics.Genre'),
        ),
        migrations.AddField(
            model_name='account',
            name='saved_films',
            field=models.ManyToManyField(to='filmfanatics.Film'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
