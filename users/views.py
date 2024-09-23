from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from university.models import Course
from users.models import User, Pay, Subscription
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaySerializer, UserCreateSerializer, UserAllSerializer, \
    SubscriptionSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserAllSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if self.request.user.pk == self.get_object().pk:
            return super().get_serializer(*args, **kwargs)
        else:
            serializer_class = UserAllSerializer
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class PayListAPIView(generics.ListAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['date_pay']
    permission_classes = [IsOwner]


class PayRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    permission_classes = [IsOwner]


class SubCreateOrDeliteAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsOwner]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data['course']
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item[0].delete()
            message = 'подписка удалена'
        else:
            subs_item = Subscription(user=user, course=course_item)
            subs_item.save()
            message = 'подписка добавлена'

        return Response({"message": message})
