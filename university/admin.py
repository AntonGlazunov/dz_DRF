from django.contrib import admin

from university.models import Course, Lesson


@admin.register(Course)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'owner')


@admin.register(Lesson)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'owner')
