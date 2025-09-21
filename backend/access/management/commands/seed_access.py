from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from access.models import AccessRule, Role, BusinessElement

User = get_user_model()


class Command(BaseCommand):
    help = "Начальные роли, элементы и правила для демонстрации"

    def handle(self, *args, **options):
        Role.objects.all().delete()
        BusinessElement.objects.all().delete()
        AccessRule.objects.all().delete()

        r_admin = Role.objects.create(name='admin',
                                      description='Administrator')
        r_manager = Role.objects.create(name='manager', description='Manager')
        r_user = Role.objects.create(name='user', description='Regular user')

        e_user = BusinessElement.objects.create(name='user',
                                                description='Users table')
        e_product = BusinessElement.objects.create(name='product',
                                                   description='Products')
        e_order = BusinessElement.objects.create(name='order',
                                                 description='Orders')

        AccessRule.objects.create(role=r_admin, element=e_user,
                                  read=True, create=True, update=True,
                                  delete=True)
        AccessRule.objects.create(role=r_admin, element=e_product,
                                  read=True, create=True, update=True,
                                  delete=True)
        AccessRule.objects.create(role=r_admin, element=e_order,
                                  read=True, create=True, update=True,
                                  delete=True)

        AccessRule.objects.create(role=r_manager, element=e_product,
                                  read=True, create=True, update=True,
                                  delete=False)
        AccessRule.objects.create(role=r_manager, element=e_order,
                                  read=True, create=True, update=True,
                                  delete=False)

        AccessRule.objects.create(role=r_user, element=e_order,
                                  read=True, create=True, update=True,
                                  delete=True)

        if not User.objects.filter(email='admin@example.com').exists():
            admin = User.objects.create_superuser(email='admin@example.com',
                                                  password='admin123',
                                                  name='Admin',
                                                  surname='Admin')
            admin.roles.add(r_admin)
            self.stdout.write(self.style.SUCCESS(
                'Created admin user: admin@example.com / admin123'))

        self.stdout.write(self.style.SUCCESS("Seeded roles/elements/rules"))
