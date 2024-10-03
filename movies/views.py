from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
import requests

from rating.models import Rating
# Create your views here.

from movies.models import Movie, Person

def search(request):
    movies = Movie.objects.all()
    return render(request,"movies/movieslist.html",{'movies':movies})

def register_model(request,title):
    api="e5f1fd02"
    url = f"https://www.omdbapi.com/?s={title}&apikey={api}"

    response = requests.get(url)
    movie_data = response.json()
    if movie_data["Response"] != 'False':
        print(movie_data)

        if Movie.objects.filter(title=movie_data['Title']).exists():
            return HttpResponse("Exists")
        else:

            director, director_created = Person.objects.get_or_create(name=movie_data["Director"])
            writer, writer_created = Person.objects.get_or_create(name=movie_data["Writer"])

            movie = Movie(
                title=movie_data['Title'],
                poster=movie_data['Poster'],
                director = director,
                writer = writer,
            )
            movie.save()
            print(request.session['current_rating'])
            return render(request,"movies/movieslist.html",{'rating':get_object_or_404(Rating,pk=request.session['current_rating']), 'movies':[movie]})
    else:
        return HttpResponse(movie_data['Error'])

def director_page(request,director):
    print(director)
    director_model = get_object_or_404(Person,name=director)
    movies = director_model.directed_movies.all()
    return render(request,'movies/director.html',{"movies":movies})
