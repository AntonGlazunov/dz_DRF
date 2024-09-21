from rest_framework import generics

from users.models import User, Pay
from users.serializers import UserSerializer, PaySerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PayListAPIView(generics.ListAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()


class PayRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()
