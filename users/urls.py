from django.urls import path
from users import views


urlpatterns = [
    path('registration/', views.RegistrationAPIView.as_view()),
    path('authorization/', views.AuthAPIView.as_view()),
    path('confirm/', views.confirm_user_code)
]