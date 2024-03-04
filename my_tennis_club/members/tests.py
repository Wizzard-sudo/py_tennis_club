import json

from django.test import TestCase
from django.urls import reverse

from .models import Member


def create_member(name, surname, email, mobile_phone):
    return Member.objects.create(name=name, surname=surname, email=email, mobile_phone=mobile_phone)


class MembersModelTests(TestCase):
    def test_should_return_empty_response(self):
        response = self.client.get(reverse("members:members"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')

    def test_should_return_list_of_members(self):
        create_member('John', 'Dou', 'john.dou@test.com', '1234567')
        create_member('Max', 'Pain', 'max.pain@test.com', '7654321')
        members = Member.objects.all().values()
        expected_json = json.dumps(list(members))

        response = self.client.get(reverse("members:members"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_json)
