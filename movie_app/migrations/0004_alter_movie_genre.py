# Generated by Django 4.1.2 on 2022-11-11 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_genre_movie_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, to='movie_app.genre'),
        ),
    ]
