from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('openAI.env')
client = OpenAI(api_key=os.environ.get('openai_apikey'))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

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

def recommend(request):
    recommended_movies = []
    prompt = ""
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        if prompt:
            # Generar embedding del prompt
            response = client.embeddings.create(
                input=[prompt],
                model="text-embedding-3-small"
            )
            prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)
            
            # Calcular similitudes para todas las películas
            movies_with_similarity = []
            for movie in Movie.objects.exclude(emb=None):
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                sim = cosine_similarity(prompt_emb, movie_emb)
                movies_with_similarity.append((movie, sim))
            
            # Ordenar por similitud y tomar las top 5
            movies_with_similarity.sort(key=lambda x: x[1], reverse=True)
            recommended_movies = movies_with_similarity[:5]
            
    return render(request, "recommend.html", {
        "prompt": prompt,
        "recommended_movies": recommended_movies,
    })



