from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import BlacklistedToken


@shared_task
def cleanup_blacklisted_tokens() -> None:
    """
    Очистка токенов из чёрного списка старше 1 дня
    :return: None
    """

    expiration_date = timezone.now() + timedelta(days=1)
    BlacklistedToken.objects.filter(
        blacklisted_at__lt=expiration_date).delete()
