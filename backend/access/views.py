from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Role, BusinessElement, AccessRule, BusinessItem
from .serializers import (RoleSerializer, BusinessElementSerializer,
                          AccessRuleSerializer, BusinessItemSerializer)
from .permissions import HasAccessPermission, IsSuperOrHasRoleAdmin


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления ролями пользователей.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperOrHasRoleAdmin]


class BusinessElementViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления бизнес-элементами.
    """

    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperOrHasRoleAdmin]


class AccessRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления правилами доступа.
    """

    queryset = AccessRule.objects.select_related('role', 'element').all()
    serializer_class = AccessRuleSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperOrHasRoleAdmin]


class BusinessItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с объектами бизнес-логики (BusinessItem).
    """

    queryset = BusinessItem.objects.select_related('element', 'owner').all()
    serializer_class = BusinessItemSerializer
    permission_classes = [permissions.IsAuthenticated, HasAccessPermission]

    def get_queryset(self):
        """
        Возвращает список объектов, доступных пользователю.
        """

        queryset = super().get_queryset()

        if self.request.user.is_superuser:
            return queryset

        user_roles = self.request.user.roles.all()
        accessible_elements = AccessRule.objects.filter(
            role__in=user_roles,
            read=True,
        ).values_list('element_id', flat=True)

        result = queryset.filter(element_id__in=accessible_elements)

        if result.exists():
            return result

        raise PermissionDenied


    def perform_create(self, serializer) -> None:
        """
        Создаёт новый объект `BusinessItem`, автоматически назначая владельца.

        :param serializer: Сериализатор для сохранения объекта.
        :return: None
        """

        serializer.save(owner=self.request.user)
