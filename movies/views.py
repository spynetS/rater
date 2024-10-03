from django.contrib.auth.views import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
import requests
import json

from rating.views import setmovie

from rating.models import Rating
# Create your views here.

from movies.models import Movie, Person

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
        writer, writer_created = Person.objects.get_or_create(name=movie_data["Writer"])

        movie,movie_created = Movie.objects.get_or_create(
            title=movie_data['Title'],
            poster=movie_data['Poster'],
            director = director,
            writer = writer,
        )
        movie.save()
        rating.movie = movie
        rating.save()

    return render(request,"movies/poster.html",{"movie":movie})
from django.db.models import Avg, F, ExpressionWrapper, FloatField
def director_page(request,director):
    print(director)
    director_model = get_object_or_404(Person,name=director)
    movies = director_model.directed_movies.all()
    movie_with_ratings = movies.annotate(
        avg_look=Avg('rating__look'),
        avg_script=Avg('rating__script'),
        avg_acting=Avg('rating__acting'),
        avg_soundtrack=Avg('rating__soundtrack'),
        avg_overalscore=Avg('rating__overalscore'),
        avg_bonus=Avg('rating__bonus'),
        avg_total=Avg(
            ExpressionWrapper(
                (F('rating__look') + F('rating__script') + F('rating__acting') + F('rating__soundtrack') + F('rating__overalscore') + F('rating__bonus')) / 5,
                output_field=FloatField()
            )
        )
    ).values(
        'id', 'title','poster', 'avg_look', 'avg_script', 'avg_acting', 'avg_soundtrack', 'avg_overalscore','avg_bonus', 'avg_total'
    )
    print(movie_with_ratings)

    return render(request,'movies/director.html',{"movies":movie_with_ratings})
