from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from university.models import Course, Lesson
from university.paginators import UniversityPaginator
from university.serializers import CourseSerializer, LessonSerializer
from university.tasks import mailing
from users.permissions import IsOwner, IsModer, IsAuthenticatedAndNoModer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = UniversityPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        instance = self.get_object()
        mailing.delay(instance)


    def get_queryset(self):
        if self.request.user.groups.filter(name='Moder').exists():
            return Course.objects.all()
        else:
            lesson = Course.objects.filter(owner=self.request.user)
            return lesson

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticatedAndNoModer]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsModer | IsOwner]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedAndNoModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = UniversityPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='Moder').exists():
            return Lesson.objects.all()
        else:
            lesson = Lesson.objects.filter(owner=self.request.user)
            return lesson


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
