from rest_framework import serializers

from university.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    count_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'preview', 'description', 'lesson', 'count_lesson']

    def get_count_lesson(self, instance):
        return len(instance.lesson_set.all())
