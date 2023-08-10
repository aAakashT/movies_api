from django.urls import path
from .views import MoviesList, CreateCollectionView, GetOneCollection, RequestCountView, CountResetView
urlpatterns = [
    path('movies/', MoviesList.as_view(), name='movies'),
    path('collection/', CreateCollectionView.as_view(), name='collection'),
    path('collection/<int:collection_uuid>/', GetOneCollection.as_view(), name='collection'),
    path('request-count/', RequestCountView.as_view(), name='count'),
    path('request-count/reset/', CountResetView.as_view(), name='CountResetView'),
]