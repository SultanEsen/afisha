from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Director, Movie, Review, Genre


# class MovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = 'title director'.split()


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['movie'] = instance.movie.title
    #
    #     return response


class MovieListSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = 'id title description director genre reviews rating'.split()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['director'] = instance.director.name
        return response

    def get_genre(self, obj_movie):
        return [genre.name for genre in obj_movie.genre.all()]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text'.split()


class ReviewListSerializer(serializers.ModelSerializer):
    # movie = MovieSerializer()

    class Meta:
        model = Review
        fields = 'id text stars movie'.split()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['movie'] = instance.movie.title
        return response


class MoviesReviewsSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True)
    reviews = serializers.SerializerMethodField()      # string of reviews.text
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title reviews rating'.split()

    def get_reviews(self, obj_movie):
        return [review.text for review in obj_movie.reviews.all()]

    def get_rating(self, obj_movie):
        summa = 0
        for s in obj_movie.reviews.all():
            summa += s.stars
        return round(summa / obj_movie.reviews.count(), 1) if obj_movie.reviews.count() else "No rating"


class DirectorsMoviesSerializers(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()  # string of movies.title

    class Meta:
        model = Director
        fields = 'id name movies'.split()

    def get_movies(self, obj_director):
        return [movie.title for movie in obj_director.movies.all()]


class MovieBaseValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=255)
    description = serializers.CharField()
    duration = serializers.FloatField(min_value=0.5, max_value=3)
    director = serializers.IntegerField(min_value=1)
    genre = serializers.ListField(child=serializers.IntegerField(min_value=1))

    @property
    def movie_data(self):
        return {
            'title': self.validated_data.get('title'),
            'description': self.validated_data.get('description'),
            'duration': self.validated_data.get('duration'),
            'director_id': self.validated_data.get('director'),
        }

    def validate_director(self, director):
        try:
            Director.objects.get(id=director)
        except Director.DoesNotExist:
            raise ValidationError(f'Director with id={director} not found')
        return director

    def validate_genre(self, genre):  # list of id
        genres_from_db = Genre.objects.filter(id__in=genre)
        # genres_from_db_all = Genre.objects.all()
        if len(genre) != genres_from_db.count():
            # list_of_genres = list(genres_from_db_all)
            # print(list_of_genres)
            # genres_not_exist = []
            # for g in genre:
            #     if g not in list_of_genres:
            #         genres_not_exist.append(g)
            raise ValidationError(f'Genre(s) Not Found')
        return genre




class MovieCreateSerializer(MovieBaseValidateSerializer):
    def validate_title(self, title):
        if Movie.objects.filter(title=title):
            raise ValidationError('Title must be unique')
        return title


class MovieUpdateSerializer(MovieBaseValidateSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = 'id name'.split()