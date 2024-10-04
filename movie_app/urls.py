from django.urls import path
from movie_app import views



urlpatterns = [
    path('movies/', views.MovieListAPIView.as_view()),
    path('directors/', views.DirectorListAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('movies/<int:id>/', views.MovieDetailListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailListAPIView.as_view()),

]