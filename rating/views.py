from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from movies.models import Movie
from rating.models import Rating

# Create your views here.

def setmovie(request,rating_id):
    rating = get_object_or_404(Rating,pk=rating_id)
    rating.movie = get_object_or_404(Movie,pk=int(request.POST['movie']))
    rating.save()
    return render(request,"rating/values.html",{"rating":rating})

def movielist(request,rating_id):
    rating = get_object_or_404(Rating,pk=rating_id)
    movies = Movie.objects.filter(title=request.POST['search'])
    if len(movies) > 0:
        return render(request,"movies/movieslist.html",{'rating':rating,'movies':movies})
    return HttpResponse(f"<button hx-post='/movie/register/{request.POST['search']}' hx-swap='beforebegin' class='btn btn-primary' >Register new movie</button>")


@login_required
def setvalues(request,rating_id):
    rating = get_object_or_404(Rating,pk=rating_id)
    rating.look = request.POST['look']
    rating.script = request.POST['script']
    rating.acting = request.POST['acting']
    rating.soundtrack = request.POST['soundtrack']
    rating.bonus = request.POST['bonus']
    rating.overalscore = request.POST['overalscore']
    rating.description = request.POST['description']
    rating.save()
    movies = Movie.objects.all()
    return render(request,"movies/movieslist.html",{'rating':rating,'movies':movies})

def values(request,rating_id):
    return render(request,"rating/values.html",{"rating":get_object_or_404(Rating,pk=rating_id)})
