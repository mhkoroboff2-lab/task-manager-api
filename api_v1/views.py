from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Tag, Project, Task
from .serializers import TagSerializer, ProjectSerializer, TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с тегами.
    
    Поддерживает все CRUD-операции, включая массовое создание,
    обновление и удаление. Фильтрация списка возможна по GET-параметру `name`.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Фильтрация тегов по имени."""
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    def list(self, request, *args, **kwargs):
        """GET-список всех тегов."""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """GET-детальный просмотр одного тега."""
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одного или нескольких тегов."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-полное обновление одного тега или списка тегов."""
        many = isinstance(request.data, list)
        if many:
            instances = [Tag.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одного тега или списка тегов."""
        many = isinstance(request.data, list)
        if many:
            instances = [Tag.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одного тега или списка через параметр `ids`."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Tag.objects.filter(id__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с проектами.
    
    Поддерживает все CRUD-операции, включая массовые создание,
    обновление и удаление. Фильтрация списка возможна по GET-параметру `name`.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        """Фильтрация проектов по названию."""
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    def list(self, request, *args, **kwargs):
        """GET-список всех проектов."""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """GET-детальный просмотр одного проекта."""
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одного или нескольких проектов."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-полное обновление одного проекта или списка проектов."""
        many = isinstance(request.data, list)
        if many:
            instances = [Project.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одного проекта или списка проектов."""
        many = isinstance(request.data, list)
        if many:
            instances = [Project.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одного проекта или списка через параметр `ids`."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Project.objects.filter(id__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с задачами.
    
    Поддерживает все CRUD-операции, включая массовые создание,
    обновление и удаление. Фильтрация возможна по project_id, status, priority, tag.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        """Фильтрация задач по различным параметрам."""
        qs = super().get_queryset()
        project_id = self.request.query_params.get('project_id')
        status_param = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        tag = self.request.query_params.get('tag')
        
        if project_id:
            qs = qs.filter(project_id=project_id)
        if status_param:
            qs = qs.filter(status=status_param)
        if priority:
            qs = qs.filter(priority=priority)
        if tag:
            qs = qs.filter(tags__name__icontains=tag)
        return qs

    def list(self, request, *args, **kwargs):
        """GET-список всех задач."""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """GET-детальный просмотр одной задачи."""
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """POST-создание одной или нескольких задач."""
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """PUT-полное обновление одной задачи или списка задач."""
        many = isinstance(request.data, list)
        if many:
            instances = [Task.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH-частичное обновление одной задачи или списка задач."""
        many = isinstance(request.data, list)
        if many:
            instances = [Task.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE-удаление одной задачи или списка через параметр `ids`."""
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Task.objects.filter(id__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)