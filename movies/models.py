from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.TextField()

class Movie(models.Model):
    title =    models.TextField()
    poster =   models.TextField()

    imdbID =   models.TextField()

    director = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='directed_movies',null=True)
    writer =   models.ForeignKey(Person,on_delete=models.CASCADE,related_name='writen_movies',null=True)

    def __str__(self):
        return self.title
