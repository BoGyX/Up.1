from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
import logging


# Настройка логгера
logger = logging.getLogger('admin_actions')

class CustomPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            # Логируем действие администратора
            action = f"Админ {request.user.username} выполнил {request.method} на {request.path}"
            logger.info(action)
        return super().has_permission(request, view)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100