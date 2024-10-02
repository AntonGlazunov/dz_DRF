from datetime import datetime, date
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from university.models import Course
from users.models import User, Pay, Subscription
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaySerializer, UserCreateSerializer, UserAllSerializer, \
    SubscriptionSerializer, PayCreateSerializer, MyTokenObtainPairSerializer
from users.services import create_session_stripe


class LoginAPIView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=request.data['email'])
            user.last_login = date.today()
            user.save()
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True, last_login=date.today())
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

    @extend_schema(
        parameters=[
            UserAllSerializer,  # serializer fields are converted to parameters
        ],
        request=UserAllSerializer,
        responses={200: UserAllSerializer},
    )
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


class PayCreateAPIView(generics.CreateAPIView):
    serializer_class = PayCreateSerializer
    queryset = Pay.objects.all()

    def perform_create(self, serializer):
        paid = serializer.save(owner=self.request.user)
        if paid.paid_course is not None:
            paid.sum_paid = paid.paid_course.price
        else:
            paid.sum_paid = paid.paid_lesson.price
        if paid.payment_method == "card":
            response = create_session_stripe(paid.paid_course.stripe_price_id)
            paid.url_paid = response['url']
        paid.save()


class PayListAPIView(generics.ListAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
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
