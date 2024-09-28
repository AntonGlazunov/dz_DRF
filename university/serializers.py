import stripe
from django.conf import settings
from rest_framework import serializers

from university.models import Course, Lesson
from university.validators import VideoURLValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'course', 'video_URL']
        validators = [VideoURLValidator(field='video_URL')]

    def create(self, validated_data):
        lesson_item = Lesson.objects.create(**validated_data)
        stripe.api_key = settings.STRIPE_API_KEY
        stripe_product = stripe.Product.create(name=lesson_item.title)
        stripe_price = stripe.Price.create(
            currency="usd",
            unit_amount=lesson_item.price*100,
            product=stripe_product['id']
        )
        lesson_item.stripe_id = stripe_product['id']
        lesson_item.stripe_price_id = stripe_price['id']
        lesson_item.save()
        return lesson_item


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    count_lesson = serializers.SerializerMethodField()
    sub = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'lesson', 'count_lesson', 'sub']

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        stripe.api_key = settings.STRIPE_API_KEY
        stripe_product = stripe.Product.create(name=course.title)
        stripe_price = stripe.Price.create(
            currency="usd",
            unit_amount=course.price,
            product=stripe_product['id']
        )
        course.stripe_id = stripe_product['id']
        course.stripe_price_id = stripe_price['id']
        course.save()
        return course

    def get_count_lesson(self, instance):
        return len(instance.lesson_set.all())

    def get_sub(self, instance):
        user = self.context['request'].user
        subs_item = instance.sub_course.filter(user=user)
        return subs_item.exists()

