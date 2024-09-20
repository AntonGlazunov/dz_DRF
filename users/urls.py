from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='users_create'),
    path('', UserListAPIView.as_view(), name='users_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='users_detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='users_update'),
    path('delite/<int:pk>/', UserDestroyAPIView.as_view(), name='users_delite'),
]