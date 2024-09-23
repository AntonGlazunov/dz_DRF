from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class SubscriptionAPITestCase(APITestCase):

    def setUp(self) -> None:
        user = User.objects.create(email='test@mail.com')
        moder = User.objects.create(email='test@mail.com')
        moder.groups.add(Group.objects.get(name='Moder'))
        moder.save()
