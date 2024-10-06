from django.contrib import admin

# Register your models here.

from movies.models import Movie, Person

admin.site.register(Movie)
admin.site.register(Person)
