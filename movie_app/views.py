from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director,Movie,Review
from .serializers import DirectorSerializer,MovieSerializer,ReviewSerializer,DirectorValidateSerializer,MovieValidateSerializer,ReviewValidateSerializer
from rest_framework import status



@api_view(['GET' , 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        movies_data = MovieSerializer(movies,many=True).data
        return Response(data=movies_data)
    elif request.method == 'POST':
        movie_serializer = MovieValidateSerializer(data=request.data)
        if not movie_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=movie_serializer.errors)
        title = movie_serializer.validated_data.get('title')
        description = movie_serializer.validated_data.get('description')
        duration = movie_serializer.validated_data.get('duration')
        director_id = movie_serializer.validated_data.get('director_id')

        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id
        )
        return Response(status=status.HTTP_201_CREATED,
                        data=MovieSerializer(movie).data)

@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        directors_data = DirectorSerializer(directors,many=True).data
        return Response(data=directors_data)
    elif request.method == 'POST':
        director_serializer = DirectorValidateSerializer(data=request.data)
        if not director_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=director_serializer.errors)
        name = director_serializer.validated_data.get('name')


        director = Director.objects.create(
            name=name
        )
        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(director).data)

@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        reviews_data = ReviewSerializer(reviews,many=True)
        return Response(data=reviews_data)
    elif request.method == 'POST':
        review_serializer = ReviewValidateSerializer(data=request)
        if not review_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=review_serializer.errors)
        text = review_serializer.validated_data.get('text')
        movie_id = review_serializer.validated_data.get('movie_id')
        stars = review_serializer.validated_data.get('stars')

        review = Review.objects.create(
            movie_id=movie_id,
            stars=stars,
            text=text
        )
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)




@api_view(['GET' , 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        movie_data = MovieSerializer(movie, many=False).data
        return Response(data=movie_data)
    elif request.method == 'PUT':
        movie_serializer = MovieSerializer(data=request.data)
        movie_serializer.is_valid(raise_exception=True)

        movie.title = movie_serializer.validated_data.get('title')
        movie.description = movie_serializer.validated_data.get('description')
        movie.duration = movie_serializer.validated_data.get('duration')
        movie.director_id = movie_serializer.validated_data.get('director_id')
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=MovieSerializer(movie).data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET' , 'PUT', 'DELETE'])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        director_data = DirectorSerializer(director, many=False).data
        return Response(data=director_data)
    elif request.method == 'PUT':
        director_serializer = DirectorSerializer(data=request.data)
        director_serializer.is_valid(raise_exception=True)

        director.name = director_serializer.validated_data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(director).data)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET' , 'PUT', 'DELETE'])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        review_data = ReviewSerializer(review, many=False).data
        return Response(data=review_data)
    elif request.method == 'PUT':
        review_serializer = ReviewSerializer(data=request.data)
        review_serializer.is_valid(raise_exception=True)

        review.text = review_serializer.validated_data.get('text')
        review.movie_id = review_serializer.validated_data.get('movie_id')
        review.stars = review_serializer.validated_data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def get_review_texts(request, movie_id):
    # Получаем отзывы для конкретного фильма по его ID
    reviews = Review.objects.filter(movie_id=movie_id)

    # Проверяем, есть ли отзывы для данного фильма
    if not reviews.exists():
        return Response({'error': 'Отзывы не найдены для указанного фильма'}, status=404)

    # Сериализуем отзывы
    serializer = ReviewSerializer(reviews, many=True)

    # Извлекаем текст отзывов из сериализованных данных
    review_texts = [review['text'] for review in serializer.data]

    # Возвращаем текст отзывов в формате JSON
    return Response(review_texts)