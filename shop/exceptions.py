from rest_framework.exceptions import APIException


class PaymentFailed(APIException):
    status_code = 400
    default_detail = '결제를 실패헀습니다.'
    default_code = 'payment_failed'
