from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        json_file_path = 'movie/management/commands/movies.json' 
        
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        # Add movies to the database
        for i in range(100):
            movie = movies[i]
            exist = Movie.objects.filter(title=movie['title']).first()
            if not exist:
                try:              
                    Movie.objects.create(
                        title=movie['title'],
                        image='movie/images/default.jpg',
                        genre=movie['genre'],
                        Released=f"{movie['year']}-01-01",  # Convertir año a fecha
                        description=movie['plot'],
                        duration=120,  # Valor por defecto 2 horas
                        rating=5.0,    # Valor por defecto rating neutro
                        url='',        # URL vacía
                    )
                    self.stdout.write(f'Added: {movie["title"]}')
                except Exception as e:
                    self.stdout.write(f'Error adding {movie["title"]}: {str(e)}')
            else:
                try:
                    exist.title = movie["title"]
                    exist.image = 'movie/images/default.jpg'
                    exist.genre = movie["genre"]
                    exist.Released = f"{movie['year']}-01-01"
                    exist.description = movie["plot"]
                    exist.save()
                    self.stdout.write(f'Updated: {movie["title"]}')
                except Exception as e:
                    self.stdout.write(f'Error updating {movie["title"]}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS('Finished processing movies'))