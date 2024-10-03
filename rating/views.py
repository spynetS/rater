from email import header
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from movies.models import Movie
from rating.models import Rating

# Create your views here.

def setmovie(request,rating_id,movie_id):
    rating = get_object_or_404(Rating,pk=rating_id)
    rating.movie = get_object_or_404(Movie,pk=movie_id)
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
    response = HttpResponse()
    response['HX-Redirect'] = '/account/'  # Set the redirect URL in the header

    return response  # Return the response to the HTMX request

def values(request,rating_id):
    return render(request,"rating/values.html",{"rating":get_object_or_404(Rating,pk=rating_id)})

@login_required
def search(request):
    ratings = Rating.objects.filter(user=request.user,movie__title__icontains=request.POST['search']).order_by("-overalscore")
    return render(request,'rating/ratings_rows.html',{'ratings':ratings})
