from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        manager_group = Group.objects.create(name='Managers')
        view_recipient_permission = Permission.objects.get(codename='view_recipient')
        view_message_permission = Permission.objects.get(codename='view_message')
        view_mailing_permission = Permission.objects.get(codename='view_mailing')
        view_user_permission = Permission.objects.get(codename='view_user')
        block_user_permission = Permission.objects.get(codename='can_block_user')
        manager_group.permissions.add(
            view_recipient_permission,
            view_message_permission,
            view_mailing_permission,
            view_user_permission,
            block_user_permission,
        )
