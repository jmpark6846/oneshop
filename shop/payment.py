import uuid

from shop.exceptions import PaymentFailed


class MockPaymentService:
    @staticmethod
    def pay(data: dict, return_value=None, status=200):
        # payment api call
        if status != 200:
            raise PaymentFailed(detail="결제를 실패했습니다. 다시 시도해주세요.")

        result = return_value or {
            'payment_id': str(uuid.uuid4()),
            'amount': data['amount'],
        }

        return result
