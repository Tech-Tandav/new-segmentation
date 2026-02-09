from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Used to create a default superuser."
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.User = get_user_model()


    def handle(self, *args, **options):
        data = {'is_staff': True, 'is_superuser': True, 'is_active':True, "email":"default@gmail.com"}
        user, _created = self.User.objects.update_or_create(username="username",
                                                            defaults=data)
        user.set_password("password")
        user.save()
