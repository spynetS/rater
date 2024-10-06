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
            avg_soundtrack=Avg('soundtrack')
        )

        overall_avg_rating = (
            average_ratings['avg_look'] +
            average_ratings['avg_script'] +
            average_ratings['avg_acting'] +
            average_ratings['avg_soundtrack']
        ) / 4

        return round(overall_avg_rating,1)
    def __str__(self):
        return f"{self.name} {self.pk}"

class Movie(models.Model):
    title =    models.TextField()
    poster =   models.TextField()
    release = models.DateField()
    plot = models.TextField()
    imdbRating = models.DecimalField(decimal_places=2,max_digits=4)

    imdbID =   models.TextField()

    director = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='directed_movies',null=True)
    writer =   models.ForeignKey(Person,on_delete=models.CASCADE,related_name='writen_movies',null=True)
    actors = models.ManyToManyField(Person,related_name="acted_movies")

    def __str__(self):
        return self.title

    def get_large_poster(self):
        return self.poster.replace("300","700")
