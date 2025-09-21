from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str=None, **extra_fields):
        """
        Создание пользователя.

        :param email: Электронная почта.
        :param password: Пароль.
        :param extra_fields: Словарь дополнительных значений.
        :return: User
        """

        errors: list[str] = []

        if not email:
            errors.append('Поле email является обязательным')

        if not password:
            errors.append('Поле пароля является обязательным')

        if errors:
            raise ValueError(errors)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str=None, **extra_fields):
        """
        Создание суперпользователя.

        :param email: Электронная почта.
        :param password: Пароль.
        :param extra_fields: Словарь дополнительных значений.
        :return: User
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.

    Атрибуты:
    - name: Имя.
    - surname: Фамилия.
    - patronymic: Отчество.
    - email: Адрес электронной почты.
    - is_active: Статус пользователя.
    - is_staff: Доступ в панель администрирования.
    - is_superuser: Статус суперпользователя.
    - roles: Роли пользователя.
    """

    name = models.CharField(
        'Имя',
        max_length=50,
    )
    surname = models.CharField(
        'Фамилия',
        max_length=50,
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=50,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=100
    )
    is_active = models.BooleanField(
        'Статус пользователя',
        default=True,
    )
    is_staff = models.BooleanField(
        'Сотрудник',
        default=False,
    )
    is_superuser = models.BooleanField(
        'Суперпользователь',
        default=False,
    )
    roles = models.ManyToManyField(
        'access.Role',
        blank=True,
        related_name='users',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blacklisted_tokens'
    )
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Blacklisted token for: {self.user}'
