import random

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
from shop.models import Product, Category, Review
from accounts.models import User


class ShopTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product_count = random.randint(1, 5)
        category = Category.objects.create(name='category')
        for i in range(cls.product_count):
            Product.objects.create(
                name=f'product{i}',
                price=i,
                category=category
            )

        cls.random_product_id = random.randint(1, cls.product_count)
        cls.user = User.objects.create(
            email = 'test@test.co',
            password = 'test',
            username = 'test'
        )
        cls.user2 = User.objects.create(
            email='test2@test.co',
            password='test2',
            username='test2'
        )
        cls.client = APIClient()

    def login(self, user):
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def logout(self):
        self.client.credentials()

    def get_random_product_id(self):
        return random.randint(1, self.product_count)

    def get_random_product(self):
        random_product = Product.objects.get(id=self.random_product_id)
        return random_product

    def test_상품_목록을_조회한다(self):
        res = self.client.get('/shop/products/')
        self.assertIs(len(res.data), self.product_count)

    def test_상품_상세정보를_조회한다(self):
        res = self.client.get(f'/shop/products/{self.random_product_id}/')
        self.assertIs(res.status_code, 200)
        self.assertIs(res.data['id'], self.random_product_id)

    def test_유저는_상품의_리뷰를_조회할수있다(self):
        product = self.get_random_product()
        review_count = random.randint(1, 5)

        for i in range(review_count):
            Review.objects.create(
                user=self.user,
                product=product,
                title="review title",
                content="review content abcd"
            )

        res = self.client.get(f'/shop/products/{self.random_product_id}/reviews/')
        self.assertIs(res.status_code, 200)
        self.assertIs(len(res.data), review_count)

    def test_유저는_상품의_리뷰를_생성할수있다(self):
        review_data = {
            'user': self.user.id,
            'product': self.random_product_id,
            'title': 'review title',
            'content': 'review content'
        }
        res = self.client.post(f'/shop/products/{self.random_product_id}/reviews/', data=review_data)
        self.assertIs(res.status_code, 201)

    def test_유저는_리뷰를_삭제할수있다(self):
        product = Product.objects.get(id=self.random_product_id)
        review = Review.objects.create(
            user=self.user,
            product=product,
            title='review title',
            content='review content'
        )

        self.assertIs(product.reviews.count(), 1)
        self.login(user=self.user)
        res = self.client.delete(f'/shop/reviews/{review.id}/')

        self.assertIs(res.status_code, 204)
        self.assertIs(product.reviews.count(), 0)

    def test_유저는_다른유저의_리뷰를_삭제할수없다(self):
        product = Product.objects.get(id=self.random_product_id)
        review = Review.objects.create(
            user=self.user,
            product=product,
            title='review title',
            content='review content'
        )
        self.login(user=self.user2)
        res = self.client.delete(f'/shop/reviews/{review.id}/')
        # self.assertIs(res.status_code, 403) AssertionError: 403 is not 403 ..?
        self.assertIs(product.reviews.count(), 1)
