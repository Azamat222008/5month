from rest_framework import serializers
from .models import Director, Movie, Review



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
