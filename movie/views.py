from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

# Create your views here.
def home(request):
    #return HttpResponse('<h1>Welcome to the Movie Reviews Home Page!</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Mariana Carrasquilla'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>About Movie Reviews</h1><p>This is a project to review movies.</p>')
    return render(request, 'about.html')