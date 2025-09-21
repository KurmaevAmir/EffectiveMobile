from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from .models import BlacklistedToken


class TokenBlacklistMiddleware(MiddlewareMixin):
    """
    Middleware для проверки токенов на отозванность (черный список).

    Перед обработкой каждого запроса проверяет наличие JWT-токена в заголовке.
    Если токен присутствует и числится в таблице `BlacklistedToken`, доступ
    запрещается и возвращается ответ 401 Unauthorized.

    Исключение составляет эндпоинт `/api/auth/logout/` — он обрабатывается
    без проверки, так как именно в нем происходит добавление токена в
    черный список.
    """

    def process_request(self, request):
        if request.path == '/api/auth/logout/':
            return None

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            if BlacklistedToken.objects.filter(token=token).exists():
                return HttpResponse('Не авторизован', status=401)
        return None