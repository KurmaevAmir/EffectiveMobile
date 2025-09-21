from django.contrib.auth import get_user_model
from requests import Request

from .models import BlacklistedToken
from .serializers import ProfileSerializer
from tokenize import TokenError

from djoser.views import UserViewSet
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Эндпоинт для кастомного пользователя.
    """

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        Выполнение "мягкого" удаления.

        :param request: Данные о запросе.
        :return: Ответ - статус выполнения запроса.
        """

        user = request.user
        user.is_active = False
        user.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    """
    Выполнения выхода из аккаунта.

    Атрибуты:
    - permission_classes: Доступ к эндпоинту доступен только пользователям,
    осуществившим вход.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Метод POST-запроса, который выполняет выход пользователя.

        :param request: Данные о запросе.
        :return: Статус выполнения выхода.
        """

        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            auth_header = request.META.get('HTTP_AUTHORIZATION', '')

            if auth_header.startswith('Bearer '):
                access_token = auth_header.split(' ')[1]

                BlacklistedToken.objects.get_or_create(
                    token=access_token,
                    user=self.request.user
                )

            return Response(
                {'detail': 'Выход выполнен успешно!'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError:
            return Response(
                {'detail': 'При выполнении выхода произошла ошибка'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    Просмотр и редактирование профиля.

    Атрибуты:
    - serializer_class: Сериализатор профиля пользователя.
    - permission_classes: Доступ к эндпоинту доступен только авторизованным
     пользователям.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        """
        :return: Модель текущего пользователя.
        """

        return self.request.user
