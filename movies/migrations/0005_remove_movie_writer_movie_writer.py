# Generated by Django 5.1.1 on 2024-10-06 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_movie_actors_movie_imdbrating_movie_plot_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='writer',
        ),
        migrations.AddField(
            model_name='movie',
            name='writer',
            field=models.ManyToManyField(null=True, related_name='writen_movies', to='movies.person'),
        ),
    ]