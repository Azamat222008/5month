from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import ConfirmCode
from django.conf import settings
from rest_framework.views import APIView



class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'username or password is wrong'})


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        user = User.objects.create_user(**serializer.validated_data, is_active=False)

        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id})


def generate_and_send_code(user):
    # Генерация шестизначного кода
    code = get_random_string(length=6, allowed_chars='0123456789')

    confirm_code = ConfirmCode.objects.create(user=user, code=code)

    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код: {code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return confirm_code

def confirm_user_code(user, input_code):
    try:
        confirm_code = ConfirmCode.objects.get(user=user)
        return confirm_code.code == input_code
    except ConfirmCode.DoesNotExist:
        return False