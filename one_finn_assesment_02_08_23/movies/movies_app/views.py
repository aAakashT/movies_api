from .middleware import RequestCounterMiddleware
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import GenreSerializer, MovieSerializer, CollectionSerializer
from .models import Genre, Movie, Collection
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .api_utils import get_movies_from_api
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
# Create your views here.



class MoviesList(APIView):
    authentication_classes = []
    
    def get(self, request):
        movies = get_movies_from_api()
        return Response(movies)
    
    
class CreateCollectionView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        movies_data = request.data.pop('movies')
        movies = []    
        
        for movie_data in movies_data:
            genres = movie_data.pop("genres")
            genres_data = genres.split(",")
            
            genres = []   
            for genre_data in genres_data:
                getgenre, createdgenre = Genre.objects.get_or_create(title=genre_data)
                
                if getgenre:
                    genres.append(getgenre)
                else:
                    genres.append(createdgenre)
                        
            
            getmovie, createdmovie = Movie.objects.get_or_create(**movie_data)
            if getmovie:
                
                for i  in genres: 
                    getmovie.genres.set(genres)  
                movies.append(getmovie)
            else:
                
                for i  in genres: 
                    createdmovie.genres.set(i)  
                movies.append(createdmovie)
                        
        data = request.data["user"] = request.user
        data = request.data
        try:
            data = Collection.objects.create(**data)
        except Exception as E:
            return Response({"exception": str(E)}, status=status.HTTP_400_BAD_REQUEST)
            
        data.movies.set(movies)
        data = data.uuid 
        data = {'collection_uuid':data}
        return Response(data, status=status.HTTP_201_CREATED)


    def get(self, request, **kwargs):
        user_collections = Collection.objects.filter(user=request.user)
        
        genre_count = Genre.objects.annotate(movie_count=Count('movie')).order_by('-movie_count')[:3]
        favorite_genres = ", ".join([genre.title for genre in genre_count])
        
        response_data = {
            "is_success": True,
            "data": {
                "collections": CollectionSerializer(user_collections, many=True).data,
                "favorite_genres": favorite_genres,
            }
        }
        
        return Response(data=response_data, status=status.HTTP_200_OK)

class GetOneCollection(APIView):
    permission_classes =  [IsAuthenticated, ]
    def get(self, request, collection_uuid):
            try:
                collection = Collection.objects.get(uuid=collection_uuid)
            except Collection.DoesNotExist:
                return Response({"error": "collection with that uuid dose not extist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"data": str(collection)}, status=status.HTTP_200_OK)
                
    def put(self, request, collection_uuid):
        try:
            collection = Collection.objects.get(uuid=collection_uuid, user=request.user)
        except Collection.DoesNotExist:
            return Response({"error":"collection dose not exits"}, status=status.HTTP_400_BAD_REQUEST)
        
        collection.title = request.data.get('title', collection.title)                   
        collection.description = request.data.get('description', collection.description)
        
        movies_data = request.data.get('movies', [])
        movies = []    
        if movies_data:
        
            for movie_data in movies_data:
                genres = movie_data.pop("genres")
                genres_data = genres.split(",")

                genres = []   
                for genre_data in genres_data:
                    getgenre, createdgenre = Genre.objects.get_or_create(title=genre_data)
                    
                    if getgenre:
                        genres.append(getgenre)
                    else:
                        genres.append(createdgenre)
                            
                getmovie, createdmovie = Movie.objects.get_or_create(**movie_data)
                if getmovie:
                    
                    for i  in genres: 
                        getmovie.genres.set(genres)  
                    movies.append(getmovie)
                else:
                    for i  in genres: 
                        createdmovie.genres.set(i)  
                    movies.append(createdmovie)
            collection.movies.clear()                   
            collection.movies.set(movies)
        collection.save()
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    def delete(self, request, collection_uuid):
        try:
            collection= Collection.objects.get(uuid=collection_uuid, user=request.user)
        except Collection.DoesNotExist:
            return Response({"error":  "collection dose not exists"}, status=status.HTTP_400_BAD_REQUEST)
        collection.delete()
        return Response({"sucess": "collection deleted sucessfully"}, status =status.HTTP_202_ACCEPTED)
    
class RequestCountView(APIView):
    def get(self, request):
        request_count = RequestCounterMiddleware.get_request_count()
        data = {"requests": request_count}
        return Response(data, status= status.HTTP_200_OK)

class CountResetView(APIView):
    def post(self, request):
        try:
            with RequestCounterMiddleware._lock:
                RequestCounterMiddleware._counter = 0
                data = {"message": "request count reset successfully"}
                return Response(data, status=status.HTTP_200_OK)
        except Exception as E:
            data = {"message": "error"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        