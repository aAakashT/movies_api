from rest_framework import serializers
from .models import Movie, Genre, Collection

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'description']