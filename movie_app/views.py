from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director,Movie,Review
from .serializers import DirectorSerializer,MovieSerializer,ReviewSerializer
from rest_framework import status



@api_view(['GET'])
def movie_list_view(request):
    movies = Movie.objects.all()
    movies_data = MovieSerializer(movies,many=True).data
    return Response(data=movies_data)

@api_view(['GET'])
def director_list_view(request):
    directors = Director.objects.all()
    directors_data = DirectorSerializer(directors,many=True).data
    return Response(data=directors_data)

@api_view(['GET'])
def review_list_view(request):
    reviews = Review.objects.all()
    reviews_data = ReviewSerializer(reviews,many=True)
    return Response(data=reviews_data)




@api_view(['GET'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    movie_data = MovieSerializer(movie, many=False).data
    return Response(data=movie_data)

@api_view(['GET'])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    director_data = DirectorSerializer(director, many=False).data
    return Response(data=director_data)


@api_view(['GET'])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    review_data = ReviewSerializer(review, many=False).data
    return Response(data=review_data)
