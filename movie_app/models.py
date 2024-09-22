from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField()  # in minutes
    director = models.ForeignKey(Director, related_name='movies', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


STARS = (
    (i, i * '*') for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=STARS, default=1)


    def __str__(self):
        return f"Review for {self.movie.title}"
