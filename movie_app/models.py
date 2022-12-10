from django.db import models


class Director(models.Model):
    """Model for director"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    genre = models.ManyToManyField(Genre, blank=True, null=True)

    def __str__(self):
        return f' movie: {self.title}, director: {self.director}, {self.genre}, ' \
               f'{self.duration}, {self.description}'

    @property
    def rating(self):
        count = self.reviews.all().count()
        sum_ = sum([i.stars for i in self.reviews.all()])
        try:
            return sum_/count
        except ZeroDivisionError:
            return 0



    # @property
    # def reviews_string(self):
    #     try:
    #         return [review.text for review in self.reviews.all()]
    #     except:
    #         return ''


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)

    def __str__(self):
        return f'{self.movie} - {self.text}'
