from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# two models movies and genre

class Genre(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'genres'
        verbose_name = 'genere'
        verbose_name_plural = 'genre'

    def __str__(self):
        return self.title
    
class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(to=Genre, related_name="movie") 
    uuid = models.UUIDField(auto_created=True, unique=True)

    class Meta:
        db_table = 'movie'
        verbose_name = 'collection'
        verbose_name_plural = 'collections'

    def __str__(self):
        return self.title
    
class Collection(models.Model):    
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    movies = models.ManyToManyField(to=Movie)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='collection')
    uuid = models.UUIDField(auto_created=True, unique=True, default=11111111112222)

    class Meta:
        db_table = 'collection'
        verbose_name = 'collection'
        verbose_name_plural = 'collections'

    def __str__(self):
        return self.title
    
    def get_top_3_genres():
        pass

    
    