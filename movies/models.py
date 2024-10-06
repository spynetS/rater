from django.db import models
from django.db.models import Avg

# Create your models here.
class Person(models.Model):
    name = models.TextField()

    def get_average_director(self):
        return self.__get_average(self.directed_movies.all())

    def get_average_writer(self):
        return self.__get_average(self.writen_movies.all())

    def __get_average(self,movies):

        from rating.models import Rating
        average = 0

        average_ratings = Rating.objects.filter(movie__id__in=[movie.pk for movie in movies]).aggregate(
            avg_look=Avg('look'),
            avg_script=Avg('script'),
            avg_acting=Avg('acting'),
            avg_soundtrack=Avg('soundtrack'),
            avg_bonus=Avg('bonus'),
            avg_overalscore=Avg('overalscore')
        )

        overall_avg_rating = (
            average_ratings['avg_look'] +
            average_ratings['avg_script'] +
            average_ratings['avg_acting'] +
            average_ratings['avg_soundtrack'] +
            average_ratings['avg_bonus'] +
            average_ratings['avg_overalscore']
        ) / 5

        return round(overall_avg_rating,1)
    def __str__(self):
        return f"{self.name} {self.pk}"

class Category(models.Model):
    value = models.TextField()

class Movie(models.Model):
    title =    models.TextField()
    poster =   models.TextField()
    release = models.DateField()
    plot = models.TextField()
    imdbRating = models.DecimalField(decimal_places=2,max_digits=4)

    imdbID =   models.TextField()

    directors = models.ManyToManyField(Person,related_name='directed_movies',null=True)
    writers   = models.ManyToManyField(Person,related_name='writen_movies',null=True)

    actors = models.ManyToManyField(Person,related_name="acted_movies")
    categories = models.ManyToManyField(Category,related_name="movies")

    def __str__(self):
        return self.title

    def get_average_rating(self):
        from rating.models import Rating
        from django.db.models import Avg, F, ExpressionWrapper, IntegerField

        rating = Rating.objects.filter(movie=self).annotate(
            avg_look=Avg('look'),
            avg_script=Avg('script'),
            avg_acting=Avg('acting'),
            avg_soundtrack=Avg('soundtrack'),
            avg_overalscore=Avg('overalscore'),
            avg_bonus=Avg('bonus'),
            avg_total=ExpressionWrapper(
                (F('look') + F('script') + F('acting') + F('soundtrack') + F('overalscore') + F('bonus')) / 5,
                output_field=IntegerField()
            )
        )[0]
        return rating

    def get_average_rating_5(self):
        from rating.models import Rating
        from django.db.models import Avg, F, ExpressionWrapper, IntegerField

        rating = Rating.objects.filter(movie=self).annotate(
            avg_look=Avg('look')/ (2),
            avg_script=Avg('script')/ (2),
            avg_acting=Avg('acting')/ (2),
            avg_soundtrack=Avg('soundtrack')/ (2),
            avg_overalscore=Avg('overalscore')/ (2),
            avg_bonus=Avg('bonus')/ (2),
            avg_total=ExpressionWrapper(
                (F('look') + F('script') + F('acting') + F('soundtrack') + F('overalscore') + F('bonus')) / (5*2),
                output_field=IntegerField()
            )
        )[0]
        return rating

    def get_large_poster(self):
        return self.poster.replace("300","700")

