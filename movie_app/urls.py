from django.urls import path
from movie_app import views



urlpatterns = [
    path('', views.movie_list_view),
    path('', views.director_list_view),
    path('', views.review_list_view),
    path('<int:id>/', views.movie_detail_view),
    path('<int:id>/', views.director_detail_view),
    path('<int:id>/', views.review_detail_view),
]