import hashlib

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from payments import PaymentStatus
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.send_sms_func import sent_sms_base
from api.permissions import IsClient
from common.order.models import Order, OrderStatus, PaymentTypes, PaymentStatus as OrderPaymentStatus
from common.payment.click.models import Payment
from common.payment.payme.models import Payment as AsPayment
from common.payment.payme.models import PaymentType, PaymentStatus as PPaymentStatus
from config.settings.base import env


# @csrf_exempt
# def prepare(request):
#     return utils.prepare(request)
#
#
# @csrf_exempt
# def complete(request):
#     return utils.complete(request)


def isset(data, columns):
    for column in columns:
        if data.get(column, None):
            return False
    return True


def paymentLoad(id):
    try:
        return Payment.objects.get(id=id)
    except:
        return None


def click_secret_key():
    PAYMENT_VARIANTS = settings.PAYMENT_VARIANTS
    _click = PAYMENT_VARIANTS['click']
    secret_key = _click[1]['secret_key']
    return secret_key


class PaymentClick(APIView):
    permission_classes = [IsClient]

    def get(self, request):
        id = request.query_params.get('id')
        if id is None:
            return Response({"error": "Order id does not found"}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(id=id, user=request.user).first()
        if order is None:
            return Response({"error": "Order does not found"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(user_id=request.user.id,
                                         order=order,
                                         total=order.totalAmount,
                                         description="Kale Gallery",
                                         billing_first_name=request.user.name,
                                         billing_last_name=request.user.name,
                                         billing_address_1="Toshkent",
                                         billing_address_2='Toshkent',
                                         billing_city='Tashkent',
                                         billing_postcode='1000000',
                                         billing_country_code='47',
                                         billing_country_area='Asia',
                                         billing_email='kale@gmail.com')

        # payment = Payment.objects.create(user=request.user,
        #                                  order=order,
        #                                  amount=order.totalAmount,
        #                                  paymentType=PaymentType.CLICK)
        context = {
            'merchant_id': env('CLICK_MERCHANT_ID'),
            'service_id': env('CLICK_SERVICE_ID'),
            'amount': payment.total,
            'transaction_param': payment.id
        }
        #https://my.click.uz/services/pay?service_id=28420&merchant_id=11369&amount=6000&transaction_param=2&return_url=https://www.youtube.com/watch?v=lF5jQkz_OyY&card_type=humo
        return Response(context, status=status.HTTP_200_OK)


class PaymentPrepareAPIView(CreateAPIView):

    def create(self, request, *args, **kwargs):
        sent_sms_base(105, "Payment Prepare", '+998901321921')
        paymentID = request.data.get('merchant_trans_id', None)
        result = self.click_webhook_errors(request)
        payment = paymentLoad(paymentID)
        if result['error'] == '0' and payment:
            payment.status = PaymentStatus.WAITING
            payment.save()
        result['click_trans_id'] = request.data.get('click_trans_id', None)
        result['merchant_trans_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_confirm_id'] = request.data.get('merchant_trans_id', None)
        return Response(result, status=status.HTTP_200_OK)

    def click_webhook_errors(self, request):
        click_trans_id = request.data.get('click_trans_id', None)
        service_id = request.data.get('service_id', None)
        click_paydoc_id = request.data.get('click_paydoc_id', None)
        paymentID = request.data.get('merchant_trans_id', None)
        amount = request.data.get('amount', None)
        action = request.data.get('action', None)
        error = request.data.get('error', None)
        error_note = request.data.get('error_note', None)
        sign_time = request.data.get('sign_time', None)
        sign_string = request.data.get('sign_string', None)
        merchant_prepare_id = request.data.get('merchant_prepare_id', None) if action != None and action == '1' else ''
        if isset(request.data,
                 ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note',
                  'sign_time',
                  'sign_string']) or (
            action == '1' and isset(request.data, ['merchant_prepare_id'])):
            return {
                'error': '-8',
                'error_note': 'Error in request from click'
            }

        signString = '{}{}{}{}{}{}{}{}'.format(
            click_trans_id, service_id, click_secret_key(), paymentID, merchant_prepare_id, amount, action, sign_time
        )
        encoder = hashlib.md5(signString.encode('utf-8'))
        signString = encoder.hexdigest()

        if signString != sign_string:
            return {
                'error': '-1',
                'error_note': 'SIGN CHECK FAILED!'
            }

        if action not in ['0', '1']:
            return {
                'error': '-3',
                'error_note': 'Action not found'
            }

        payment = paymentLoad(paymentID)
        if payment is None:
            return {
                'error': '-5',
                'error_note': 'User does not exist'
            }
        if abs(float(amount) - float(payment.total) > 0.01):
            return {
                'error': '-2',
                'error_note': 'Incorrect parameter amount'
            }

        if payment.status == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

        if action == '1':
            if paymentID != merchant_prepare_id:
                return {
                    'error': '-6',
                    'error_note': 'Transaction not found'
                }

        if payment.status == PaymentStatus.REJECTED or int(error) < 0:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }
        return {
            'error': '0',
            'error_note': 'Success'
        }


class PaymentCompleteAPIView(CreateAPIView):

    def create(self, request, *args, **kwargs):
        sent_sms_base(105, "Payment Complate", '+998901321921')
        paymentID = request.data.get('merchant_trans_id', None)
        payment = paymentLoad(paymentID)
        result = self.click_webhook_errors(request)
        if request.data.get('error', None) != None and int(request.data.get('error', None)) < 0 and payment:
            payment.status = PaymentStatus.REJECTED
            payment.save()
        if result['error'] == '0' and payment:
            payment.status = PaymentStatus.CONFIRMED
            payment.save()

            order = Order.objects.get(id=payment.order.id)
            order.status = OrderStatus.PENDING
            order.paymentStatus = OrderPaymentStatus.PAID
            order.paymentType = PaymentTypes.CLICK
            order.save()

            AsPayment.objects.create(
                user=order.user,
                order=order,
                amount=payment.amount,
                paymentType=PaymentType.CLICK,
                status=PPaymentStatus.CONFIRMED
            )

        result['click_trans_id'] = request.data.get('click_trans_id', None)
        result['merchant_trans_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = request.data.get('merchant_prepare_id', None)
        result['merchant_confirm_id'] = request.data.get('merchant_prepare_id', None)
        return Response(result)

    def click_webhook_errors(self, request):
        click_trans_id = request.data.get('click_trans_id', None)
        service_id = request.data.get('service_id', None)
        click_paydoc_id = request.data.get('click_paydoc_id', None)
        paymentID = request.data.get('merchant_trans_id', None)
        amount = request.data.get('amount', None)
        action = request.data.get('action', None)
        error = request.data.get('error', None)
        error_note = request.data.get('error_note', None)
        sign_time = request.data.get('sign_time', None)
        sign_string = request.data.get('sign_string', None)
        merchant_prepare_id = request.data.get('merchant_prepare_id', None) if action != None and action == '1' else ''
        if isset(request.data,
                 ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note',
                  'sign_time',
                  'sign_string']) or (
            action == '1' and isset(request.data, ['merchant_prepare_id'])):
            return {
                'error': '-8',
                'error_note': 'Error in request from click'
            }

        signString = '{}{}{}{}{}{}{}{}'.format(
            click_trans_id, service_id, click_secret_key(), paymentID, merchant_prepare_id, amount, action, sign_time
        )
        encoder = hashlib.md5(signString.encode('utf-8'))
        signString = encoder.hexdigest()

        if signString != sign_string:
            return {
                'error': '-1',
                'error_note': 'SIGN CHECK FAILED!'
            }

        if action not in ['0', '1']:
            return {
                'error': '-3',
                'error_note': 'Action not found'
            }

        payment = paymentLoad(paymentID)
        if not payment:
            return {
                'error': '-5',
                'error_note': 'User does not exist'
            }
        if abs(float(amount) - float(payment.total) > 0.01):
            return {
                'error': '-2',
                'error_note': 'Incorrect parameter amount'
            }

        if payment.status == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

        if action == '1':
            if paymentID != merchant_prepare_id:
                return {
                    'error': '-6',
                    'error_note': 'Transaction not found'
                }

        if payment.status == PaymentStatus.REJECTED or int(error) < 0:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }
        return {
            'error': '0',
            'error_note': 'Success'
        }
