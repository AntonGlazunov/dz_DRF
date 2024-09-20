from university.apps import UniversityConfig
from rest_framework.routers import DefaultRouter

from university.views import CourseViewSet, LessonViewSet

app_name = UniversityConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'lesson', LessonViewSet, basename='lesson')

urlpatterns = [

] + router.urls
