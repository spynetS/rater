from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.TextField()

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
