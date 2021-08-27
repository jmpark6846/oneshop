import random
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from shop.models import Category


class BackTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create(
            email='test@test.co',
            password='test',
            username='test',
            is_staff=True
        )

    def login(self, user):
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def logout(self):
        self.client.credentials()

    def test_일반_유저는_백오피스_유저API에_접근할수없다(self):
        self.staff_user.is_staff = False
        self.staff_user.save()

        self.login(self.staff_user)
        res = self.client.get('/back/users/')
        assert_status_code_is_403 = res.status_code == 403
        self.assertIs(assert_status_code_is_403, True)

        self.staff_user.is_staff = True
        self.staff_user.save()
        res = self.client.get('/back/users/')
        assert_status_code_is_403 = res.status_code == 403
        self.assertIs(assert_status_code_is_403, False)

    def test_상품_생성시_이미지를_여러개_업로드_할수있다(self):
        self.login(self.staff_user)
        category = Category.objects.create(
            name='test_category'
        )

        image_files = []
        for i in range(random.randint(0, 5)):
            file = SimpleUploadedFile(
                f'test_image_file_{i}.jpg',
                b'test_image_contents_as_bytes',
                content_type='image/jpeg'
            )
            image_files.append(file)

        data = {
            'name': 'test',
            'price': 5000,
            'category': category.id,
            'image_files': image_files
        }

        res = self.client.post('/back/products/', data=data)
        self.assertIs(res.status_code, 201)
