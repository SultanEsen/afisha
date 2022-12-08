from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Director, Movie, Review, Genre
from .serializers import (
    DirectorListSerializer, MovieListSerializer,
    ReviewListSerializer, MoviesReviewsSerializer,
    DirectorsMoviesSerializers, MovieCreateSerializer,
    MovieUpdateSerializer, GenreSerializer
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def static_data_view(request):
    dict_ = {
        'text': 'Hello, World!'
    }
    return Response(data=dict_)


@api_view(['GET'])
def main_page(request):
    dict_ = {
        'text': 'main page',
        'pages': [{'page_1': 'http://127.0.0.1:8000/api/v1/directors/'},
                  {'page_2': 'http://127.0.0.1:8000/api/v1/movies/'},
                  {'page_3': 'http://127.0.0.1:8000/api/v1/reviews/'},
                  {'page_4': 'http://127.0.0.1:8000/api/v1/movies/reviews/'},
                  {'page_5': 'http://127.0.0.1:8000/api/v1/directors/movies/'},
                  ]
    }
    return Response(data=dict_)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def directors_view(request):
    directors = Director.objects.all()
    data = DirectorListSerializer(directors, many=True).data
    return Response(data=data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movies_view(request):
    print(request.user)
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieListSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = MovieCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'data with errors',
                    'errors': serializer.errors
                }
            )
        movie = Movie.objects.create(
                **serializer.movie_data
                # title=request.data.get('title'),
                # description=request.data.get('description'),
                # duration=request.data.get('duration'),
                # director_id=request.data.get('director'),
            )
        movie.genre.set(request.data.get('genre'))
        movie.save()
        print(movie)
        return Response(status=status.HTTP_201_CREATED,
                        data={
                            "message": "Successfully created"
                        }
                        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reviews_view(request):
    reviews = Review.objects.all()
    data = ReviewListSerializer(reviews, many=True).data
    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movies_reviews_view(request):
    movies_reviews = Movie.objects.all()
    data = MoviesReviewsSerializer(movies_reviews, many=True).data
    return Response(data=data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def directors_movies_view(request):
    directors_movies = Director.objects.all()
    data = DirectorsMoviesSerializers(directors_movies, many=True).data
    return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def movie_item_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Movie not found'})
    if request.method == 'GET':
        serializer = MovieListSerializer(movie)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={
                            'message': 'Movie successfully removed'
                        }
                        )
    else:
        serializer = MovieUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director')
        movie.genre.set(request.data.get('genre'))
        movie.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'Successfully updated',
                'movie': MovieListSerializer(movie).data
            }
        )


class GenreListAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class GenreItemUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'id'
