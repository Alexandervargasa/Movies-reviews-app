from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movie/images/')
    Released = models.DateField(default='2000-01-01')
    url = models.URLField(blank=True)
    genre = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()  # Duración en minutos
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Calificación de 0.0 a 10.0

    def __str__(self):
        return self.title

    @property
    def duration_human(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        return f"{hours}h {minutes}min" if hours else f"{minutes}min"