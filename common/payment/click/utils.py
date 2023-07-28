import hashlib

from django.conf import settings
from django.http import JsonResponse
from payments import PaymentStatus

from common.order.models import Checkout, Order
from common.payment.payme.models import Payment


def isset(data, columns):
    for column in columns:
        if data.get(column, None):
            return False
    return True


def paymentLoad(id):
    return Payment.objects.get(id=id)


def click_secret_key():
    PAYMENT_VARIANTS = settings.PAYMENT_VARIANTS
    _click = PAYMENT_VARIANTS['click']
    secret_key = _click[1]['secret_key']
    return secret_key


def click_webhook_errors(request):
    click_trans_id = request.POST.get('click_trans_id', None)
    service_id = request.POST.get('service_id', None)
    click_paydoc_id = request.POST.get('click_paydoc_id', None)
    paymentID = request.POST.get('merchant_trans_id', None)
    amount = request.POST.get('amount', None)
    action = request.POST.get('action', None)
    error = request.POST.get('error', None)
    error_note = request.POST.get('error_note', None)
    sign_time = request.POST.get('sign_time', None)
    sign_string = request.POST.get('sign_string', None)
    merchant_prepare_id = request.POST.get('merchant_prepare_id', None) if action != None and action == '1' else ''
    if isset(request.POST,
             ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note', 'sign_time',
              'sign_string']) or (
        action == '1' and isset(request.POST, ['merchant_prepare_id'])):
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
    if abs(float(amount) - float(payment.amount) > 0.01):
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


def prepare(request):
    if request.method == "POST":
        paymentID = request.POST.get('merchant_trans_id', None)
        result = click_webhook_errors(request)
        payment = paymentLoad(paymentID)
        if result['error'] == '0':
            payment.status = PaymentStatus.WAITING
            payment.save()
        result['click_trans_id'] = request.POST.get('click_trans_id', None)
        result['merchant_trans_id'] = request.POST.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = request.POST.get('merchant_trans_id', None)
        result['merchant_confirm_id'] = request.POST.get('merchant_trans_id', None)
        return JsonResponse(result)
    else:
        return JsonResponse({'status': 'not accepted'})


def complete(request):
    paymentID = request.POST.get('merchant_trans_id', None)
    payment = paymentLoad(paymentID)
    result = click_webhook_errors(request)
    if request.POST.get('error', None) != None and int(request.POST.get('error', None)) < 0:
        payment.status = PaymentStatus.REJECTED
        payment.save()
    if result['error'] == '0':
        payment.status = PaymentStatus.CONFIRMED
        payment.save()

        checkout = Checkout.objects.filter(user=payment.user).first()
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
        payment.orders.set(orders)
        payment.save()

        # REMOVE CART PRODUCTS FROM CHECKOUT
        for i in checkout.products.select_related('cart', 'product').all():
            i.delete()
    result['click_trans_id'] = request.POST.get('click_trans_id', None)
    result['merchant_trans_id'] = request.POST.get('merchant_trans_id', None)
    result['merchant_prepare_id'] = request.POST.get('merchant_prepare_id', None)
    result['merchant_confirm_id'] = request.POST.get('merchant_prepare_id', None)
    return JsonResponse(result)
