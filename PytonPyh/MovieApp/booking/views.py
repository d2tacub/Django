from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Fetch all movies to display in the dropdown
    movies = Movie.objects.all()
    if request.method == "POST":
        movie_id = request.POST.get("movie")
        seat = request.POST.get("seat")
        movie = Movie.objects.get(id=movie_id)

        # Create the ticket and redirect to the ticket page
        ticket = Ticket.objects.create(movie=movie, user=request.user, seat=seat)
        return redirect("ticket", ticket_id=ticket.id)

    return render(request, "booking/home.html", {"movies": movies})

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Ticket

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "booking/login.html", {"error": "Invalid username or password"})
    return render(request, "booking/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    movies = Movie.objects.all()
    if request.method == "POST":
        movie_id = request.POST.get("movie")
        seat = request.POST.get("seat")
        movie = Movie.objects.get(id=movie_id)
        ticket = Ticket.objects.create(movie=movie, user=request.user, seat=seat)
        return redirect("ticket", ticket_id=ticket.id)
    return render(request, "booking/home.html", {"movies": movies})

@login_required
def ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, "booking/ticket.html", {"ticket": ticket})

