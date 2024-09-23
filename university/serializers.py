from rest_framework import serializers

from university.models import Course, Lesson
from university.validators import VideoURLValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'course', 'video_URL']
        validators = [VideoURLValidator(field='video_URL')]


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    count_lesson = serializers.SerializerMethodField()
    sub = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'lesson', 'count_lesson', 'sub']

    def get_count_lesson(self, instance):
        return len(instance.lesson_set.all())

    def get_sub(self, instance):
        user = self.context['request'].user
        subs_item = instance.sub_course.filter(user=user)
        return subs_item.exists()
