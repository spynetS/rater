from django.contrib.auth.views import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
import requests
from datetime import datetime
import json
from django.db.models import Avg, F, ExpressionWrapper, FloatField

from rating.views import setmovie

from rating.models import Rating
# Create your views here.

from movies.models import Movie, Person, Category

def search(request):
    movies = Movie.objects.all()
    return render(request,"movies/movieslist.html",{'movies':movies})

def search_api(request):
    api="e5f1fd02"
    print(request.POST['search'])
    url = f"https://www.omdbapi.com/?s={request.POST['search']}&apikey={api}"
    response = requests.get(url)
    movie_data = response.json()
    if movie_data["Response"] != 'False':
        movies = movie_data['Search']
        for movie in movies:
            movie['json'] = json.dumps(movie)
        return render(request,'movies/movieslist.html',{'movies':movies})
    return HttpResponse("No movie with that name was found");


@login_required
def register_movie(request,rating_id):
    rating = get_object_or_404(Rating,pk=rating_id)

    api="e5f1fd02"
    movie_data = json.loads(request.POST['movie'])
    imdbID = movie_data['imdbID']

    if not Movie.objects.filter(imdbID=imdbID).exists():
        url = f"https://www.omdbapi.com/?i={imdbID}&apikey={api}"
        response = requests.get(url)
        movie_data = response.json()


        director, director_created = Person.objects.get_or_create(name=movie_data["Director"])

        movie,movie_created = Movie.objects.get_or_create(
            title=movie_data['Title'],
            poster=movie_data['Poster'],
            release = datetime.strptime(movie_data['Released'],"%d %b %Y"),
            plot = movie_data['Plot'],
            imdbRating = float(movie_data['imdbRating']),
            imdbID = imdbID
        )
        movie.save()

        actors = movie_data['Actors'].replace('"',"").split(",")
        for actor in actors:
            print(actor.strip())
            actor_model, actor_created = Person.objects.get_or_create(name=actor.strip())
            movie.actors.add(actor_model)

        writers = movie_data['Writer'].replace('"',"").split(",")
        for writer in writers:
            print(writer.strip())
            writer_model, writer_created = Person.objects.get_or_create(name=writer.strip())
            movie.writers.add(writer_model)

        directors = movie_data['Director'].replace('"',"").split(",")
        for director in directors:
            print(director.strip())
            director_model, director_created = Person.objects.get_or_create(name=director.strip())
            movie.directors.add(director_model)

        genres = movie_data['Genre'].replace('"',"").split(",")
        for genre in genres:
            print(genre.strip())
            category_model, category_created = Category.objects.get_or_create(value=genre.strip())
            movie.categories.add(category_model)


        rating.movie = movie
        rating.save()
    response = render(request,"movies/poster.html",{"movie":movie})
    response.headers["HX-Trigger"] = "MovieSelected"
    return response


def director_page(request,director):
    director_model = get_object_or_404(Person,name=director)
    movies = director_model.directed_movies.all()
    # Retrieve ratings for all movies directed by this director
    ratings = Rating.objects.filter(movie__in=movies).annotate(
        avg_look=Avg('look'),
        avg_script=Avg('script'),
        avg_acting=Avg('acting'),
        avg_soundtrack=Avg('soundtrack'),
        avg_overalscore=Avg('overalscore'),
        avg_bonus=Avg('bonus'),
        avg_total=ExpressionWrapper(
            (F('look') + F('script') + F('acting') + F('soundtrack') + F('overalscore') + F('bonus')) / 5,
            output_field=FloatField()
        )
    )

    return render(request,'movies/director.html',{"director":director_model,"ratings":ratings})

@login_required
def movie(request,movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    return render(request,'movies/movie.html',{'movie':movie})
