from rest_framework import serializers

from users.models import User, Pay, Subscription
from users.services import create_session_stripe


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['course']


class PayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['date_pay', 'paid_course', 'paid_lesson', 'sum_paid', 'payment_method', 'status_paid']


class UserSerializer(serializers.ModelSerializer):
    pay_owner = PayUserSerializer(many=True, read_only=True)
    sub_user = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'country', 'pk', 'pay_owner', 'sub_user']


class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['paid_course', 'paid_lesson', 'payment_method']

class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['paid_course', 'paid_lesson', 'payment_method', 'sum_paid', 'status_paid', 'url_paid']



