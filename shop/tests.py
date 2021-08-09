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

        cls.product_id = random.randint(1, cls.product_count)
        cls.user = User.objects.create(
            email = 'test@test.co',
            password = 'test',
            username = 'test'
        )
        cls.client = APIClient()

    def test_상품_목록을_조회한다(self):
        res = self.client.get('/shop/product/')
        self.assertIs(len(res.data), self.product_count)

    def test_상품_상세정보를_조회한다(self):
        res = self.client.get(f'/shop/product/{self.product_id}/')
        self.assertIs(res.status_code, 200)
        self.assertIs(res.data['id'], self.product_id)

    def test_유저는_상품의_리뷰를_조회할수있다(self):
        product = Product.objects.get(id=self.product_id)
        review_count = random.randint(1, 5)

        for i in range(review_count):
            Review.objects.create(
                author=self.user,
                product=product,
                title="review title",
                content="review content abcd"
            )

        res = self.client.get(f'/shop/product/{self.product_id}/reviews/')
        self.assertIs(res.status_code, 200)
        self.assertIs(len(res.data), review_count)

    def test_유저는_상품의_리뷰를_생성할수있다(self):
        review_data = {
            'author': self.user.id,
            'title': 'review title',
            'content': 'review content'
        }
        res = self.client.post(f'/shop/product/{self.product_id}/reviews_create/', data=review_data)
        self.assertIs(res.status_code, 200)

    def test_유저는_자신이_쓴_상품의_리뷰만_삭제할수있다(self):
        product = Product.objects.get(id=self.product_id)
        review = Review.objects.create(
            author=self.user,
            product=product,
            title='review title',
            content='review content'
        )

        self.assertIs(product.reviews.count(), 1)
        refresh_token = RefreshToken.for_user(self.user)
        access_token = refresh_token.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        res = self.client.delete(f'/shop/reviews/{review.id}/')
        self.assertIs(res.status_code, 204)
        self.assertIs(product.reviews.count(), 0)