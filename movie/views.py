from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

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

def signup(request):
    email= request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request): 
    matplotlib.use('Agg') 
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')  # Obtener todos los años de las películas 
    movie_counts_by_year = {}  # Crear un diccionario para almacenar la cantidad de películas por año  
    for year in years: # Contar la cantidad de películas por año 
        if year: 
            movies_in_year = Movie.objects.filter(year=year) 
        else: 
            movies_in_year = Movie.objects.filter(year__isnull=True) 
            year = "None" 
        count = movies_in_year.count() 
        movie_counts_by_year[year] = count 
    bar_width = 0.5 # Ancho de las barras 
    bar_spacing = 0.5 # Separación entre las barras  
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras 

# Crear la gráfica de barras 
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center') 
    # Personalizar la gráfica 
    plt.title('Movies per year') 
    plt.xlabel('Year') 
    plt.ylabel('Number of movies') 
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90) 
    # Ajustar el espaciado entre las barras 
    plt.subplots_adjust(bottom=0.3) 
    # Guardar la gráfica en un objeto BytesIO 
    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
     
    # Convertir la gráfica a base64 
    image_png = buffer.getvalue() 
    buffer.close() 
    graphic = base64.b64encode(image_png) 
    graphic = graphic.decode('utf-8') 

    # ==========================
    # Películas por género (solo primer género)
    # ==========================
    movies = Movie.objects.all()
    movie_counts_by_genre = {}
    for movie in movies:
        if movie.genre:  
            first_genre = movie.genre.split(',')[0].strip()  # solo el primer género
        else:
            first_genre = "None"
        movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    # Crear gráfica por género
    plt.bar(range(len(movie_counts_by_genre)), movie_counts_by_genre.values(), width=0.5, color='orange') 
    plt.title('Movies per Genre (first genre only)') 
    plt.xlabel('Genre') 
    plt.ylabel('Number of Movies') 
    plt.xticks(range(len(movie_counts_by_genre)), movie_counts_by_genre.keys(), rotation=45, ha="right") 
    plt.tight_layout()  

    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
    graphic_genres = base64.b64encode(buffer.getvalue()).decode('utf-8') 
    buffer.close()
 
    # Renderizar la plantilla statistics.html con la gráfica 
    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic_genres': graphic_genres
    }) 

    