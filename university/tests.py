from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from university.models import Course, Lesson
from users.models import User, Subscription


class SubscriptionAPITestCase(APITestCase):

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
            'owner': 2
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
            'pk': 3,
            'title': 'pytest',
            'description': 'pytest',
            'video_URL': 'https://www.youtube.com/?app=desktop&hl=ru',
            'course': 2,
            'owner': 3
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
            'owner': 2
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
