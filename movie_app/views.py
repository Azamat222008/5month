from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director,Movie,Review
from .serializers import DirectorSerializer,MovieSerializer,ReviewSerializer
from rest_framework import status



@api_view(['GET' , 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        movies_data = MovieSerializer(movies,many=True).data
        return Response(data=movies_data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')

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
        name = request.data.get('name')


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
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        stars = request.data.get('stars')

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
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
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
        director.name = request.data.get('name')
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
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie_id')
        review.stars = request.data.get('stars')
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