from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from university.models import Course, Lesson
from users.models import User, Subscription


class LessonAPITestCase(APITestCase):

    def setUp(self) -> None:
        Group.objects.create(name='Moder')
        User.objects.create(email='moder@mail.com')
        moder = User.objects.get(email='moder@mail.com')
        moder.groups.add(Group.objects.get(name='Moder'))
        moder.save()
        User.objects.create(email='test@mail.com')
        User.objects.create(email='test1@mail.com')
        Course.objects.create(pk=1, title='test', description='test', owner=User.objects.get(email='test@mail.com'))
        Course.objects.create(pk=2, title='test1', description='test', owner=User.objects.get(email='test1@mail.com'))
        Lesson.objects.create(pk=4, title='test', description='test', owner=User.objects.get(email='test@mail.com'))
        Lesson.objects.create(pk=5, title='test1', description='test', owner=User.objects.get(email='test1@mail.com'))
        Subscription.objects.create(user=User.objects.get(email='test@mail.com'), course=Course.objects.get(pk=2))

    def test_lesson_create(self):
        '''Создание урока'''

        data = {
            'title': 'pytest',
            'description': 'pytest',
            'video_URL': 'https://asdda.com',
            'course': 2,
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'pytest',
            'description': 'pytest',
            'video_URL': 'https://asdda.com',
            'course': 2,
            'owner': 2
        }
        response = client.post(
            '/lesson/create/',
            data=data

        )

        self.assertRaises(
            ValidationError
        )

        data = {
            'title': 'pytest',
            'description': 'pytest',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 3,
        }
        response = client.post(
            '/lesson/create/',
            data=data

        )

        self.assertRaises(
            ValidationError
        )

        data = {
            'pk': 1,
            'title': 'pytest1',
            'description': 'pytest',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
        }
        response = client.post(
            '/lesson/create/',
            data=data

        )

        self.assertEqual(
            response.json(),
            {'title': 'pytest1', 'description': 'pytest', 'course': 2,
             'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru'}
        )

        self.assertTrue(
            Lesson.objects.filter(title='pytest1').exists()
        )

    def test_lesson_list(self):
        response = self.client.get('/lesson/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/lesson/')

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [{'course': None, 'description': 'test',
                                                                      'title': 'test', 'video_URL': None}]}

        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/lesson/')

        self.assertEqual(
            response.json(),
            {'count': 2, 'next': None, 'previous': None, 'results': [{'course': None, 'description': 'test',
                                                                      'title': 'test', 'video_URL': None},
                                                                     {'course': None, 'description': 'test',
                                                                      'title': 'test1', 'video_URL': None}
                                                                     ]}
        )

    def test_lesson_detail(self):
        response = self.client.get('/lesson/4/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/lesson/4/')

        self.assertEqual(
            response.json(),
            {'course': None, 'description': 'test', 'title': 'test', 'video_URL': None}
        )

        response = client.get('/lesson/5/')

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_update_put(self):
        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'pytest',
            'description': 'pytest',
            'video_URL': 'https://asdda.com',
            'course': 2,
        }
        response = client.put(
            '/lesson/update/4/',
            data=data

        )

        self.assertRaises(
            ValidationError
        )

        data = {
            'title': 'pytest11',
            'description': 'pytest',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
        }

        response = client.put(
            '/lesson/update/5/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        data = {
            'title': 'pytest11',
            'description': 'pytest',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
        }

        response = client.put(
            '/lesson/update/4/',
            data=data

        )

        self.assertEqual(
            response.json(),
            {'course': 2, 'description': 'pytest', 'title': 'pytest11',
             'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru'}

        )

        self.assertTrue(
            Lesson.objects.filter(title='pytest11').exists()
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'test',
            'description': 'test',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
        }

        response = client.put(
            '/lesson/update/4/',
            data=data

        )

        self.assertEqual(
            response.json(),
            {'course': 2, 'description': 'test', 'title': 'test',
             'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru'}

        )

        self.assertTrue(
            Lesson.objects.filter(title='test').exists()
        )

    def test_lesson_update_patch(self):
        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'pytest',
            'description': 'pytest',
            'video_URL': 'https://asdda.com',
            'course': 2,
        }
        response = client.patch(
            '/lesson/update/4/',
            data=data

        )

        self.assertRaises(
            ValidationError
        )

        data = {
            'title': 'pytest11',
            'description': 'pytest',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
        }

        response = client.patch(
            '/lesson/update/5/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        data = {
            'title': 'pytest11',
            'description': 'pytest',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
        }

        response = client.patch(
            '/lesson/update/4/',
            data=data

        )

        self.assertEqual(
            response.json(),
            {'course': 2, 'description': 'pytest', 'title': 'pytest11',
             'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru'}

        )

        self.assertTrue(
            Lesson.objects.filter(title='pytest11').exists()
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'test',
            'description': 'test',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
        }

        response = client.put(
            '/lesson/update/4/',
            data=data

        )

        self.assertEqual(
            response.json(),
            {'course': 2, 'description': 'test', 'title': 'test',
             'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru'}

        )

        self.assertTrue(
            Lesson.objects.filter(title='test').exists()
        )

    def test_lesson_delite(self):
        response = self.client.delete(
            '/lesson/delite/4/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(
            '/lesson/delite/5/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        response = client.delete(
            '/lesson/delite/4/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertTrue(
            not Lesson.objects.filter(pk=4).exists()
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(
            '/lesson/delite/5/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class CourseAPITestCase(APITestCase):

    def setUp(self) -> None:
        Group.objects.create(name='Moder')
        User.objects.create(email='moder@mail.com')
        moder = User.objects.get(email='moder@mail.com')
        moder.groups.add(Group.objects.get(name='Moder'))
        moder.save()
        User.objects.create(email='test@mail.com')
        User.objects.create(email='test1@mail.com')
        Course.objects.create(pk=4, title='test', description='test', owner=User.objects.get(email='test@mail.com'))
        Course.objects.create(pk=5, title='test1', description='test', owner=User.objects.get(email='test1@mail.com'))
        Lesson.objects.create(pk=4, title='test', description='test', owner=User.objects.get(email='test@mail.com'))
        Lesson.objects.create(pk=5, title='test1', description='test', owner=User.objects.get(email='test1@mail.com'))
        Subscription.objects.create(user=User.objects.get(email='test1@mail.com'), course=Course.objects.get(pk=5))

    def test_course_create(self):
        '''Создание курса'''

        data = {
            'title': 'pytest',
            'description': 'pytest',
        }

        response = self.client.post(
            '/course/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'pytest',
            'description': 'pytest',
        }

        response = client.post(
            '/course/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertRaises(
            ValidationError
        )

        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'pytest',
            'description': 'pytest',
        }
        response = client.post(
            '/course/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'count_lesson': 0, 'description': 'pytest', 'lesson': [], 'sub': False, 'title': 'pytest'}
        )

        self.assertTrue(
            Course.objects.filter(title='pytest').exists()
        )

    def test_course_list(self):
        response = self.client.get('/course/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/course/')

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [{'count_lesson': 0, 'description': 'test',
                                                                      'lesson': [], 'sub': False, 'title': 'test'}]}
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/course/')

        self.assertEqual(
            response.json(),
            {'count': 2, 'next': None, 'previous': None, 'results': [{'count_lesson': 0, 'description': 'test',
                                                                      'lesson': [], 'sub': False, 'title': 'test'},
                                                                     {'count_lesson': 0, 'description': 'test',
                                                                      'lesson': [], 'sub': False, 'title': 'test1'}]}
        )

    def test_course_detail(self):
        response = self.client.get('/course/4/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test1@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/course/5/')

        self.assertEqual(
            response.json(),
            {'count_lesson': 0, 'description': 'test', 'lesson': [], 'sub': True, 'title': 'test1'}
        )

        response = client.get('/course/4/')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_lesson_update_put(self):
        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'pytest',
            'description': 'pytest',
        }
        response = client.put(
            '/course/5/',
            data=data

        )

        self.assertRaises(
            ValidationError
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        data = {
            'title': 'pytest11',
            'description': 'pytest',
        }

        response = client.put(
            '/course/4/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count_lesson': 0, 'description': 'pytest', 'lesson': [], 'sub': False, 'title': 'pytest11'}
        )

        self.assertTrue(
            Course.objects.filter(title='pytest11').exists()
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'test',
            'description': 'test',
        }

        response = client.put(
            '/course/5/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count_lesson': 0, 'description': 'test', 'lesson': [], 'sub': False, 'title': 'test'}

        )

        self.assertTrue(
            Course.objects.filter(title='test').exists()
        )

    def test_course_update_patch(self):
        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'pytest',
            'description': 'pytest',
        }
        response = client.patch(
            '/course/5/',
            data=data

        )

        self.assertRaises(
            ValidationError
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        data = {
            'title': 'pytest11',
            'description': 'pytest',
        }

        response = client.patch(
            '/course/4/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count_lesson': 0, 'description': 'pytest', 'lesson': [], 'sub': False, 'title': 'pytest11'}

        )

        self.assertTrue(
            Course.objects.filter(title='pytest11').exists()
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'title': 'test',
            'description': 'test',
        }

        response = client.patch(
            '/course/5/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count_lesson': 0, 'description': 'test', 'lesson': [], 'sub': False, 'title': 'test'}

        )

        self.assertTrue(
            Course.objects.filter(title='test').exists()
        )

    def test_course_delite(self):
        response = self.client.delete(
            '/course/5/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(
            '/course/5/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        response = client.delete(
            '/course/4/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertTrue(
            not Course.objects.filter(pk=1).exists()
        )

        user = User.objects.get(email='moder@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(
            '/course/5/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
