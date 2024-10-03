from django.contrib.auth.views import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm
from django.contrib import messages
from .models import Account


# Create your views here.
from rating.models import Rating
from .forms import CustomSignUpForm

@login_required
def index(request):
    ratings = Rating.objects.filter(user=request.user,movie__isnull=False).order_by("-overalscore")
    return render(request,'accounts/index.html',{'ratings':ratings})

@login_required
def add(request):
    rating = Rating(user=request.user)
    rating.save()
    request.session['current_rating'] = rating.pk

    return render(request,"accounts/add.html",{'rating':rating})

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/account')  # Redirect to the home page or any other page
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            account = Account(user=user)
            account.save()
            login(request, user)  # Automatically log the user in
            messages.success(request, 'Account created successfully!')
            return redirect('/account')  # Redirect to home or any page after sign up
    else:
        form = CustomSignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def settings(request):
    return render(request,"accounts/settings.html",{})
