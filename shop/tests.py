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
        products = []
        for i in range(cls.product_count):
            product = Product.objects.create(
                name=f'product{i}',
                price=(i+1)*1000,
                category=category
            )
            products.append(product)

        # cls.random_product_id
        cls.random_product = random.choice(products)
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
        return random.choice(Product.objects.all())

    def test_상품_목록을_조회한다(self):
        res = self.client.get('/shop/products/')
        self.assertEqual(len(res.data), self.product_count)

    def test_상품_상세정보를_조회한다(self):
        res = self.client.get(f'/shop/products/{self.random_product.id}/')
        self.assertIs(res.status_code, 200)
        self.assertEqual(res.data['id'], self.random_product.id)

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

        res = self.client.get(f'/shop/products/{product.id}/reviews/')
        self.assertIs(res.status_code, 200)
        self.assertIs(len(res.data), review_count)

    def test_유저는_상품의_리뷰를_생성할수있다(self):
        self.login(self.user)
        review_data = {
            'user': self.user.id,
            'product': self.random_product.id,
            'title': 'review title',
            'content': 'review content'
        }
        res = self.client.post(f'/shop/products/{self.random_product.id}/reviews/', data=review_data)
        self.assertIs(res.status_code, 201)

    def test_유저는_리뷰를_삭제할수있다(self):
        review = Review.objects.create(
            user=self.user,
            product=self.random_product,
            title='review title',
            content='review content'
        )
        self.login(user=self.user)
        res = self.client.delete(f'/shop/reviews/{review.id}/')
        self.assertIs(res.status_code, 204)

        review.refresh_from_db()
        self.assertIsNotNone(review.deleted_at)

    def test_유저는_다른유저의_리뷰를_삭제할수없다(self):
        product = Product.objects.get(id=self.random_product.id)
        review = Review.objects.create(
            user=self.user,
            product=product,
            title='review title',
            content='review content'
        )
        self.login(user=self.user2)
        res = self.client.delete(f'/shop/reviews/{review.id}/')
        status_code_is_403 = res.status_code == 403
        self.assertTrue(status_code_is_403)
        self.assertIs(product.reviews.count(), 1)

    def test_장바구니_추가할수있다(self):
        # 로그인하지 않은 유저가 장바구니에 제품 추가
        cart_item_data = {
            'product': self.random_product.id,
            'quantity': 1,
        }
        res = self.client.post('/shop/cart/', cart_item_data)
        self.assertEqual(res.status_code, 201)

        # 로그인한 유저
        self.login(user=self.user)
        cart_item_data = {
            'product': self.random_product.id,
            'quantity': 1,
        }
        res = self.client.post('/shop/cart/', cart_item_data)
        self.assertEqual(res.status_code, 201)

        # 카트에 이미 있는 항목을 추가할 경우 수량만 추가
        cart_item_data['quantity'] = 2

        res = self.client.post('/shop/cart/', cart_item_data)
        self.assertEqual(res.status_code, 201)

        self.user.cart.refresh_from_db()
        cart: dict = self.user.cart.to_dict

        self.assertEqual(cart[self.random_product.id]['quantity'], 3)
        self.assertEqual(len(cart.keys()), 1)

    def test_장바구니_항목들을_주문하고_결제한다(self):
        self.login(user=self.user)
        cart_item_data = {
            'product': self.random_product.id,
            'quantity': 1,
        }
        self.client.post('/shop/cart/', cart_item_data)
        res = self.client.post('/shop/cart/order/')
        self.assertEqual(res.status_code, 200)

        order_id = res.data['order']
        res = self.client.post('/shop/payment/', {'order': order_id})
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.data['payment_id'])
