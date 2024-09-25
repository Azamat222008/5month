from rest_framework import serializers
from .models import Director, Movie, Review
from rest_framework.exceptions import ValidationError



class DirectorSerializer(serializers.ModelSerializer):
    count_movies = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = 'name count_movies'.split()

    def get_count_movies(self, director):
        count = director.movies.count()
        return count




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'




class MovieSerializer(serializers.ModelSerializer):
    reviews =ReviewSerializer(many=True)
    average_rating = serializers.SerializerMethodField()


    class Meta:
        model = Movie
        fields = 'title description duration director reviews average_rating'.split()



    def get_average_rating(self, movie):
        reviews = movie.reviews.all()
        if reviews:
            sum_reviews = sum(i.stars for i in reviews)
            average_rating = sum_reviews / len(reviews)
            return average_rating
        return None


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, default='no text')
    director = serializers.IntegerField(min_value=1)
    duration = serializers.IntegerField(min_value=1)

def validate_director(self, director):
    try:
        Director.objects.get(id=director)
    except:
        raise ValidationError('Director not found')
    return director

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    movie = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField(default=1)

def validate_movie(self, movie):
    try:
        Movie.objects.get(id=movie)
    except:
        raise ValidationError('Movie not found')
    return movie