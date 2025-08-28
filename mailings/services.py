import datetime

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailings.models import MailingTry


def run_mailing(mailing):
    if not mailing.sending_start:
        mailing.sending_start = datetime.datetime.now()
    mailing.sending_end = datetime.datetime.now()
    mailing.status = "Запущена"
    mailing.save()

    for recipient in mailing.recipient_list.all():
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.message,
                EMAIL_HOST_USER,
                [recipient.email]
            )
            MailingTry.objects.create(
                date_time=datetime.datetime.now(),
                status='Успешно',
                response=f'Успешная отправка на адрес: {recipient.email}',
                mailing=mailing,
            )
        except Exception as e:
            MailingTry.objects.create(
                date_time=datetime.datetime.now(),
                status='Не успешно',
                response=f'Ошибка при отправке на адрес: {recipient.email}, ошибка: {e}',
                mailing=mailing,
            )
        finally:
            mailing.save()
    # return None
