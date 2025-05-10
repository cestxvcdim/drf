from django.core.management import BaseCommand

from config.settings import CSU_EMAIL, CSU_FIRST_NAME, CSU_LAST_NAME, CSU_PASSWORD
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=CSU_EMAIL,
            first_name=CSU_FIRST_NAME,
            last_name=CSU_LAST_NAME,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(CSU_PASSWORD)
        user.save()
