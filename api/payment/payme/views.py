import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.order.models import Order, PaymentTypes, OrderStatus, PaymentStatus as OrderPaymentStatus, CartProduct
from common.payment.payme.models import Payment, PaymentType, PaymentStatus
from kale.contrib.paymeuz.config import *
from kale.contrib.paymeuz.methods import *
from kale.contrib.paymeuz.models import Transaction
from kale.contrib.paymeuz.serializers import SubscribeSerializer

User = get_user_model()

AUTHORIZATION1 = {'X-Auth': AUTHORIZATION['X-Auth'].split(':')[0]}


class CardCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_create(serializer.validated_data)
        return Response(result)

    def card_create(self, validated_data):
        data = dict(
            id=validated_data['id'],
            method=CARD_CREATE,
            params=dict(
                card=dict(
                    number=validated_data['params']['card']['number'],
                    expire=validated_data['params']['card']['expire'],
                ),
                save=validated_data['params']['save']
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION1)
        result = response.json()
        if 'error' in result:
            return result

        token = result['result']['card']['token']
        result = self.card_get_verify_code(token)
        return result

    def card_get_verify_code(self, token):
        data = dict(
            method=CARD_GET_VERIFY_CODE,
            params=dict(
                token=token
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION1)
        result = response.json()
        if 'error' in result:
            return result
        result.update(token=token)
        return result


class CardVerifyApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_verify(serializer.validated_data)
        return Response(result)

    def card_verify(self, validated_data):
        data = dict(
            id=validated_data['id'],
            method=CARD_VERIFY,
            params=dict(
                token=validated_data['params']['token'],
                code=validated_data['params']['code'],
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION1)
        result = response.json()
        return result


class PaymentApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['params']['token']
        result = self.receipts_create(token, serializer.validated_data)
        return Response(result)

    def receipts_create(self, token, validated_data):
        order = Order.objects.filter(id=validated_data.get('id')).first()
        if order is None:
            return {"status": status.HTTP_400_BAD_REQUEST}
        if order.totalAmount * 100 <= 0:
            return {"message": "Amount must be grater then zero", "status": status.HTTP_400_BAD_REQUEST}

        data = dict(
            id=validated_data['id'],
            method=RECEIPTS_CREATE,
            params=dict(
                amount=order.totalAmount * 100,
                account=dict(
                    order_id=order.id
                    # KEY_1=validated_data['params']['account'][KEY_1]
                )
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION1)
        result = response.json()
        if 'error' in result:
            return result

        trans_id = result['result']['receipt']['_id']
        trans = Transaction()
        trans.create_transaction(
            trans_id=trans_id,
            request_id=result['id'],
            amount=result['result']['receipt']['amount'],
            account=result['result']['receipt']['account'],
            status=trans.PROCESS,
        )
        result = self.receipts_pay(trans_id, token)
        return result

    def receipts_pay(self, trans_id, token):
        data = dict(
            method=RECEIPTS_PAY,
            params=dict(
                id=trans_id,
                token=token
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION)
        result = response.json()
        trans = Transaction()

        if 'error' in result:
            trans.update_transaction(
                trans_id=trans_id,
                status=trans.FAILED,
            )
            return result

        trans.update_transaction(
            trans_id=result['result']['receipt']['_id'],
            status=trans.PAID,
        )
        if not 'error' in result:
            order = Order.objects.filter(user=self.request.user).last()
            order.status = OrderStatus.PENDING
            order.paymentStatus = OrderPaymentStatus.PAID
            order.paymentType = PaymentTypes.PAYME
            order.save()

            Payment.objects.create(
                user=order.user,
                order=order,
                amount=order.totalAmount,
                paymentType=PaymentType.PAYME,
                status=PaymentStatus.CONFIRMED
            )
            cartProducts = CartProduct.objects.filter(cart__user=order.user,
                                                      product_id__in=order.products.all().select_related(
                                                          'product').values_list('product_id'))
            cartProducts.delete()
        return result
