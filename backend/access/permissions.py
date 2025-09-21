from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import AccessRule, BusinessElement, BusinessItem

User = get_user_model()

METHOD_TO_PERMISSION = {
    'GET': 'read',
    'POST': 'create',
    'PATCH': 'update',
    'PUT': 'update',
    'DELETE': 'delete',
}


class HasAccessPermission(BasePermission):
    """
    Проверка на наличие доступа к действиям с моделью бизнес-элемента.
    """

    def _get_user_permission(self, user: User,
                             element: BusinessElement) -> dict[str, bool]:
        """
        Формирует словарь доступов, которые можно предоставить пользователю.

        :param user: Пользователь, отправивший запрос.
        :param element: Элемент.
        :return: Словарь доступов.
        """

        roles = user.roles.all()
        rules = AccessRule.objects.filter(role__in=roles, element=element)

        permissions_dict = {
            'read': False,
            'create': False,
            'update': False,
            'delete': False,
        }

        for rule in rules:
            for permission in permissions_dict:
                if getattr(rule, permission):
                    permissions_dict[permission] = True

        return permissions_dict


    def has_permission(self, request: Request, view) -> bool:
        """
        Проверка наличия доступа к ресурсу на уровне списков.

        :param request: Данные о запросе.
        :param view: Представление о действии.
        :return: True если предоставить доступ, False - в обратном случае.
        """

        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True

        if request.user.is_superuser:
            return True

        perm_field = METHOD_TO_PERMISSION.get(request.method)

        if not perm_field:
            return False

        if view.action == 'create':
            element_id = request.data.get('element_id')

            try:
                element = BusinessElement.objects.get(id=element_id)
            except BusinessElement.DoesNotExist:
                return False

            user_permission = self._get_user_permission(request.user, element)
            return user_permission.get(perm_field, False)

        return True

    def has_object_permission(self, request: Request,
                              view, obj: BusinessItem) -> bool:
        """
        Проверка наличия доступа к ресурсу на уровне объекта.

        :param request: Данные о запросе.
        :param view: Представление о действии.
        :param obj: Модель бизнес-предмета.
        :return: True если предоставить доступ, False - в обратном случае.
        """

        element = obj.element

        if request.user.is_superuser:
            return True

        perm_field = METHOD_TO_PERMISSION.get(request.method)

        if not perm_field:
            return False

        user_permission = self._get_user_permission(request.user, element)
        return user_permission.get(perm_field, False)


class IsSuperOrHasRoleAdmin(permissions.BasePermission):
    """
    Проверка на доступ. Пользователь является администратором или
    суперпользователем.
    """

    def has_permission(self, request: Request, view) -> bool:
        """
        Проверка наличия доступа к ресурсу на уровне списков.

        :param request: Данные о запросе.
        :param view: Представление о действии.
        :return: True если предоставить доступ, False - в обратном случае.
        """

        if request.user.is_superuser:
            return True

        return request.user.roles.filter(name='admin').exists()
