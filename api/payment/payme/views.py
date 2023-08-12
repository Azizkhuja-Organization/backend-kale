import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.order.models import Checkout, Order
from common.payment.payme.models import Payment, PaymentType
from kale.contrib.paymeuz.config import *
from kale.contrib.paymeuz.methods import *
from kale.contrib.paymeuz.models import Transaction
from kale.contrib.paymeuz.serializers import SubscribeSerializer

User = get_user_model()

AUTHORIZATION1 = {'X-Auth': AUTHORIZATION['X-Auth'].split(':')[0]}


class CardCreateApiView(APIView):

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

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['params']['token']
        result = self.receipts_create(token, serializer.validated_data)
        return Response(result)

    def receipts_create(self, token, validated_data):
        checkout = Checkout.objects.filter(user_id=validated_data.get('id')).last()
        if checkout is None:
            return {"status": status.HTTP_400_BAD_REQUEST}
        data = dict(
            id=validated_data['id'],
            method=RECEIPTS_CREATE,
            params=dict(
                amount=checkout.amount,
                account=dict(
                    KEY_1=validated_data['params']['account'][KEY_1]
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
                token=token)
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
        print(result, "Paid")
        if not 'error' in result:
            checkout = Checkout.objects.filter(user=self.request.user).order_by('-id').first()
            if checkout.isDelivery:
                orders = [
                    Order(checkout=checkout,
                          product=i.product,
                          quantity=i.quantity,
                          totalAmount=i.amount
                          ) for i in checkout.products.select_related('cart', 'product').all()
                ]
            else:
                orders = [
                    Order(checkout=checkout,
                          product=i.product,
                          quantity=i.quantity,
                          totalAmount=i.amount
                          ) for i in checkout.products.select_related('cart', 'product').all()
                ]
            orders = Order.objects.bulk_create(orders)
            payment = Payment.objects.create(
                user=self.request.user,
                amount=checkout.amount,
                paymentType=PaymentType.PAYME
            )
            payment.orders.set(orders)
            payment.save()

            # REMOVE CART PRODUCTS FROM CHECKOUT
            # for i in checkout.products.select_related('cart', 'product').all():
                # i.delete()

        return result
