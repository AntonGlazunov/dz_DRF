from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    PayListAPIView, PayRetrieveAPIView, SubCreateOrDeliteAPIView, PayCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='users_create'),
    path('', UserListAPIView.as_view(), name='users_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='users_detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='users_update'),
    path('delite/<int:pk>/', UserDestroyAPIView.as_view(), name='users_delite'),
    path('pays/', PayListAPIView.as_view(), name='pays_list'),
    path('pays/<int:pk>/', PayRetrieveAPIView.as_view(), name='pay_detail'),
    path('pays/create/', PayCreateAPIView.as_view(), name='pays_create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sub/', SubCreateOrDeliteAPIView.as_view(), name='add/delite-sub'),
]