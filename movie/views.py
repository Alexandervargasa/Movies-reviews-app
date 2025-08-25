from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    # return HttpResponse('<h1>Welcome to Home Page</h1>')
    # return render (request,'home.html' )
    # return render (request, 'home.html', {'name':'Alexander Vargas'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
     movies = Movie.objects.all()
    return render(request, 'home.html', {'name':'Alexander Vargas', 'searchTerm':searchTerm, 'movies': movies})

def about(request):
    # return HttpResponse('<h1>Welcome to About Page</h1>')
    return render (request, 'about.html', {'name':'Alexander Vargas'})

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # === GRÁFICA POR AÑO ===
    movie_counts_by_year = {}
    for movie in all_movies:
        if movie.Released:
            year = movie.Released.year
        else:
            year = "Unknown"
            
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # Crear la primera gráfica (por año)
    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)  # 2 filas, 1 columna, primera posición
    
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # === GRÁFICA POR GÉNERO ===
    movie_counts_by_genre = {}
    for movie in all_movies:
        # Obtener solo el primer género (antes de cualquier coma o separador)
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()  # Toma el primer género y quita espacios
        else:
            first_genre = "Unknown"
            
        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    # Crear la segunda gráfica (por género)
    plt.subplot(2, 1, 2)  # 2 filas, 1 columna, segunda posición
    
    bar_positions_genre = range(len(movie_counts_by_genre))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.5, align='center', color='orange')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)

    # Ajustar el layout
    plt.subplots_adjust(hspace=0.5)

    # Guardar la gráfica combinada
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    # Convertir a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic})

def signup(request):
    email = request.POST.get('email')
    return render(request, 'signup.html', {'email':email})

def login_view(request):
    return render(request, 'login.html')