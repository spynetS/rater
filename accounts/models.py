from urllib.parse import uses_relative
from django.contrib.auth.forms import User
from django.db import models
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="accounts")
    theme = models.TextField(default="")

    friends = models.ManyToManyField(to='self')

    def get_top_director(self):
        ratings = self.get_top_movies()
        print(ratings[0].movie.directors.all())
        return ratings[0].movie.directors.all()[0]


    def get_top_movies(self):
        from rating.models import Rating
        ratings_with_average = Rating.objects.filter(user=self.user).annotate(
            avg_rating=ExpressionWrapper(
                (Coalesce(F('look'), 0) +
                Coalesce(F('script'), 0) +
                Coalesce(F('acting'), 0) +
                Coalesce(F('overalscore'), 0) +
                Coalesce(F('bonus'), 0) +
                Coalesce(F('soundtrack'), 0)) / 5,
                output_field=FloatField()
            )
        ).order_by('-avg_rating')[:3]

        print("ratings",ratings_with_average)

        return ratings_with_average

    def __str__(self):
        return self.user.username
