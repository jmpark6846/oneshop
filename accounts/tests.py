from rest_framework.test import APITestCase, APIClient
from accounts.models import User


class UserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password1': 'test12#$',
            'password2': 'test12#$',
        }
        cls.data = data

    def test_registration_회원가입하면_유저와_프로필_생성(self):
        response = self.client.post('/accounts/registration/', data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.data)

        email = response.data['user']['email']
        user = User.objects.get(email=email)
        self.assertIsNotNone(user.profile)

        access_token = response.data['access_token']

        new_client = APIClient()
        new_client.credentials(HTTP_AUTHORIZATION='JWT ' + access_token)
        response = new_client.get('/accounts/user/')
        self.assertEqual(response.status_code, 200)
