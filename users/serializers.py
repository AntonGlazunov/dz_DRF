from rest_framework import serializers

from users.models import User, Pay


class PayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['date_pay', 'paid_course', 'paid_lesson', 'sum_paid', 'payment_method']


class UserSerializer(serializers.ModelSerializer):
    pay_user = PayUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'country', 'pk', 'pay_user']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        return user


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['user', 'date_pay', 'paid_course', 'paid_lesson', 'sum_paid', 'payment_method']
