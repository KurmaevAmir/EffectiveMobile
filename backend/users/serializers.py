from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from access.models import Role
from .models import User

from djoser.serializers import UserSerializer, UserDeleteSerializer
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed


class RegistrationSerializer(UserSerializer):
    """
    Сериализатор для регистрации нового пользователя.

    Атрибуты:
    - password2: Поле для подтверждения пароля.
    """

    password2 = serializers.CharField(write_only=True, label='Повтор пароля')

    class Meta:
        model = User
        fields = ('surname', 'name', 'patronymic',
                  'email', 'password', 'password2')

    def validate(self, data):
        """
        Проверка полученных данных на правильность ввода.

        :param data: Данные полученные на вход.
        :return: Data
        """

        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return super().validate(data)

    def create(self, validated_data) -> User:
        """
        Создание объекта пользователя после регистрации.

        :param validated_data: Проверенные данные.
        :return: User.
        """

        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user


class ProfileSerializer(UserSerializer):
    """
    Сериализатор для отображения профиля пользователя.
    """

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'surname', 'name', 'patronymic', 'email', 'is_active')


class CustomJWTAuthentication(JWTAuthentication):
    """
    Кастомная аутентификация через JWT.

    Дополнительно проверяте, что пользователь активен.
    """

    def get_user(self, validated_token) -> User:
        """
        Получает пользователя из токена и проверяет его активность.

        :param validated_token: Проверенный JWT-токен.
        :return: Объект пользователя.
        :raise AuthenticationFailed: если пользователь деактивирован.
        """

        user = super().get_user(validated_token)
        if not user.is_active:
            raise AuthenticationFailed('Аккаунт удалён')
        return user


class UserAssignRolesSerializer(serializers.Serializer):
    """
    Сериализатор для назначения ролей пользователю.
    """

    role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        many=True
    )

    def update(self, instance: User, validated_data) -> User:
        """
        Присваивает пользователю новые роли.

        :param instance: Объект пользователя.
        :param validated_data: Данные с ролями.
        :return: Обновлённый объект пользователя.
        """

        roles = validated_data['role_ids']
        instance.roles.set(roles)
        instance.save()
        return instance
