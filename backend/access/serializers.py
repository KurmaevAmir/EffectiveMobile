from .models import Role, BusinessElement, AccessRule, BusinessItem

from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели ролей.
    """

    class Meta:
        model = Role
        fields = ('id', 'name', 'description')


class BusinessElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели бизнес-элементов.
    """

    class Meta:
        model = BusinessElement
        fields = ('id', 'name', 'description')


class AccessRuleSerializer(serializers.ModelSerializer):
    """
    Сериализатор правил доступа.

    Атрибуты:
    - role: Роль пользователя.
    - role_id: Идентификатор роли пользователя.
    - element: Бизнес-элемент.
    - element_id: Идентификатор бизнес-элемента.
    """

    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        write_only=True,
        source='role'
    )
    element = BusinessElementSerializer(read_only=True)
    element_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessElement.objects.all(),
        write_only=True,
        source='element'
    )

    class Meta:
        model = AccessRule
        fields = ('id', 'role', 'role_id', 'element', 'element_id',
                  'read', 'create', 'update', 'delete')


class BusinessItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор бизнес-объектов.

    Атрибуты:
    - owner: Владелец.
    - element: Бизнес-элемент.
    - element_id: Идентификатор бизнес-элемента.
    """

    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    element = BusinessElementSerializer(read_only=True)
    element_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessElement.objects.all(),
        write_only=True,
        source='element'
    )

    class Meta:
        model = BusinessItem
        fields = ('id', 'element', 'element_id', 'owner',
                  'title', 'data', 'created_at')
        read_only_fields = ('created_at',)
