from django.contrib import admin

# Register your models here.

from movies.models import Category, Movie, Person

admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Person)
