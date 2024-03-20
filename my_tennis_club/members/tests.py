from parameterized import parameterized
from django.test import TestCase
from django.urls import reverse

from .models import Member
from .serializers import MemberSerializer


def create_member(name, surname, email, mobile_phone):
    return Member.objects.create(name=name, surname=surname, email=email, mobile_phone=mobile_phone)


class MembersModelTests(TestCase):
    def test_should_return_empty_response(self):
        response = self.client.get(reverse("members:members-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')

    def test_should_return_list_of_members(self):
        create_member('John', 'Dou', 'john.dou@test.com', '1234567')
        create_member('Max', 'Pain', 'max.pain@test.com', '7654321')
        members = Member.objects.all().values()
        expected_json = MemberSerializer(list(members), many=True).data

        response = self.client.get(reverse("members:members-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(MemberSerializer(response.json(), many=True).data, expected_json)

    def test_should_save_new_member(self):
        member = Member.objects.filter(email='john.dou@test.com').first()
        self.assertIsNone(member)

        new_member = Member(name='John', surname='Dou', email='john.dou@test.com', mobile_phone='1234567')
        request_body = MemberSerializer(new_member).data

        response = self.client.post(reverse("members:members-save"), request_body, content_type="application/json")
        member = Member.objects.filter(email='john.dou@test.com').first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(member.__str__(), new_member.__str__())

    def test_should_return_error_if_member_with_the_same_email_exists(self):
        create_member('John', 'Dou', 'john.dou@test.com', '1234567')
        new_member = Member(name='John', surname='Dou', email='john.dou@test.com', mobile_phone='1234567')
        request_body = MemberSerializer(new_member).data

        self.assertEqual(Member.objects.all().count(), 1)

        response = self.client.post(reverse("members:members-save"), request_body, content_type="application/json")

        self.assertEqual(Member.objects.all().count(), 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'email': ['member with this email already exists.']})

    @parameterized.expand([(Member(surname='Dou', email='john.dou@test.com', mobile_phone='1234567'),
                            {'name': ['This field may not be blank.']}),
                           (Member(name='John', email='john.dou@test.com', mobile_phone='1234567'),
                            {'surname': ['This field may not be blank.']}),
                           (Member(name='John', surname='Dou', mobile_phone='1234567'),
                            {'email': ['This field may not be blank.']}),
                           (Member(name='John', surname='Dou', email='john.dou@test.com'),
                            {'mobile_phone': ['This field may not be blank.']}),
                           (Member(name='John', surname='Dou'),
                            {'email': ['This field may not be blank.'],
                             'mobile_phone': ['This field may not be blank.']},),
                           (Member(name='John'),
                            {'surname': ['This field may not be blank.'],
                             'email': ['This field may not be blank.'],
                             'mobile_phone': ['This field may not be blank.']}),
                           (Member(),
                            {'name': ['This field may not be blank.'],
                             'surname': ['This field may not be blank.'],
                             'email': ['This field may not be blank.'],
                             'mobile_phone': ['This field may not be blank.']})
                           ])
    def test_should_return_error_if_lack_of_required_parameters(self, member, error_dict):
        request_body = MemberSerializer(member).data

        response = self.client.post(reverse("members:members-save"), request_body, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_dict)

    def test_should_return_member_by_id(self):
        create_member('John', 'Dou', 'john.dou@test.com', '1234567')
        member = Member.objects.get(id=1)
        expected_json = MemberSerializer(member).data

        response = self.client.get(reverse("members:member-get", kwargs={'id': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(MemberSerializer(response.json()).data, expected_json)

    def test_should_return_member_not_found(self):
        response = self.client.get(reverse("members:member-get", kwargs={'id': 1}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'Member with id 1 not found')

    def test_should_return_member_by_id(self):
        create_member('John', 'Dou', 'john.dou@test.com', '1234567')
        member = Member.objects.get(id=1)
        expected_json = MemberSerializer(member).data

        response = self.client.get(reverse("members:member-get", kwargs={'id': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(MemberSerializer(response.json()).data, expected_json)

    def test_should_return_member_not_found(self):
        response = self.client.get(reverse("members:member-get", kwargs={'id': 1}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'Member with id 1 not found')

    def test_should_update_member(self):
        create_member('John', 'Dou', 'john.dou@test.com', '1234567')

        new_member = Member(name='NewJohn', surname='NewDou', email='newjohn.dou@test.com', mobile_phone='1234567')
        request_body = MemberSerializer(new_member).data

        response = self.client.put(reverse("members:members-update", kwargs={'pk': 1}), request_body,
                                   content_type="application/json")
        member = Member.objects.filter(email='newjohn.dou@test.com').first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(member.__str__(), new_member.__str__())

    def test_should_return_not_found_when_update(self):
        new_member = Member(name='NewJohn', surname='NewDou', email='newjohn.dou@test.com', mobile_phone='1234567')
        request_body = MemberSerializer(new_member).data

        response = self.client.put(reverse("members:members-update", kwargs={'pk': 1}), request_body,
                                   content_type="application/json")
        member = Member.objects.filter(email='newjohn.dou@test.com').first()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"detail":"No Member matches the given query."}')
