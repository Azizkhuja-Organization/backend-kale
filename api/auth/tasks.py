from celery import shared_task
from django.contrib.auth import get_user_model

from api.auth.send_sms_func import sent_sms_base
from common.users.models import Code

User = get_user_model()


@shared_task(name='send_sms')
def send_sms(id, phone):
    user = User.objects.get(id=id)
    code, created = Code.objects.get_or_create(user=user)
    number = code.generate_code()
    sent_sms_base(code.user.id, number, phone)


@shared_task(name='verified_user')
def verified_user(guid):
    user = User.objects.get(guid=guid)
    user.is_verified = True
    user.save()
