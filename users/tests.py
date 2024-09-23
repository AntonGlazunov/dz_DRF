from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from university.models import Course
from users.models import User, Subscription


class SubscriptionAPITestCase(APITestCase):

    def setUp(self) -> None:
        User.objects.create(email='test@mail.com')
        Course.objects.create(pk=1, title='test', description='test', owner=User.objects.get(email='test@mail.com'))
        Course.objects.create(pk=2, title='test1', description='test', owner=User.objects.get(email='test@mail.com'))
        Subscription.objects.create(user=User.objects.get(email='test@mail.com'), course=Course.objects.get(pk=2))

    def test_create_sub(self):
        """ тестирование подключение и удаление подписок """

        data = {
            'course': 2
        }
        response = self.client.post(
            '/users/sub/',
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
            'course': 1
        }
        response = client.post(
            '/users/sub/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'message': 'подписка добавлена'}
        )

        data = {
            'course': 2
        }
        response = client.post(
            '/users/sub/',
            data=data
        )

        self.assertEqual(
            response.json(),
            {'message': 'подписка удалена'}
        )
