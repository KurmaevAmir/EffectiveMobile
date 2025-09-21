from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import JSONField

User = get_user_model()


class Role(models.Model):
    """
    Модель роли.

    Атрибуты:
    - name: Название.
    - description: Описание.
    """

    name = models.CharField(
        'Название',
        max_length=50,
        unique=True
    )
    description = models.CharField('Описание', blank=True)

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    """
    Элемент приложения, на который можно назначать права.

    Атрибуты:
    - name: Название.
    - description: Описание.
    """

    name = models.CharField(
        'Название',
        max_length=100,
        unique=True
    )
    description = models.CharField('Описание', blank=True)

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    """
    Модель правила доступа.

    Атрибуты:
    - role: Роль пользователя.
    - element: Бизнес-элемент.
    - read: Правило доступа на чтение.
    - create: Правило доступа на создание.
    - update: Правило доступа на изменение.
    - delete: Правило доступа на удаление.
    """

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        related_name='access_rules'
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.SET_NULL,
        null=True,
        related_name='access_rules'
    )

    read = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'element')


    def __str__(self):
        return f'{self.role.name} - {self.element.name}'


class BusinessItem(models.Model):
    """
    Пример бизнес-объекта для демонстрации прав.

    Атрибуты:
    - element: Тип бизнес-элемента, к которому относится объект.
    - owner: Пользователь, который создал объект.
    - title: Название.
    - data: Произвольные данные.
    - created_at: Время создания.
    """

    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.SET_NULL,
        null=True,
        related_name='items'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='items'
    )
    title = models.CharField('Название', max_length=100)
    data = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.element.name} / {self.title}'
