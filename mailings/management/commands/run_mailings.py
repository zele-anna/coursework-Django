from django.core.management.base import BaseCommand
from django.db.models import Q

from mailings.models import Mailing
from mailings.services import run_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(Q(status='Создана') | Q(status='Запущена'))

        if mailings:
            for mailing in mailings:
                run_mailing(mailing)
                print(f'Рассылка ID {mailing.pk} запущена')
        else:
            'Нет ни одной рассылки для отправки.'
