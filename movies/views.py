from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
import requests

from rating.models import Rating
# Create your views here.

from movies.models import Movie

def search(request):
    movies = Movie.objects.all()
    return render(request,"movies/movieslist.html",{'movies':movies})

def register_model(request,title):
    api="e5f1fd02"
    url = f"https://www.omdbapi.com/?t={title}&apikey={api}"

    response = requests.get(url)
    movie_data = response.json()
    print(movie_data)

    if Movie.objects.filter(title=movie_data['Title']).exists():
        return HttpResponse("Exists")
    else:
        movie = Movie(
            title=movie_data['Title'],
            poster=movie_data['Poster']
        )
        movie.save()
        print(request.session['current_rating'])
        return render(request,"movies/movieslist.html",{'rating':get_object_or_404(Rating,pk=request.session['current_rating']), 'movies':[movie]})
