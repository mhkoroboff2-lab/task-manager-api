from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, ProjectViewSet, TaskViewSet

# Создаем роутер (автоматический диспетчер маршрутов)
router = DefaultRouter()

# Регистрируем наши ViewSets
# Это создаст адреса: api/v1/tags/, api/v1/projects/, api/v1/tasks/
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

# Подключаем маршруты роутера
urlpatterns = [
    path('', include(router.urls)),
]