from django.contrib import admin
from mailings.models import Recipient, Message, Mailing, MailingTry


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
    )
    search_fields = ("subject", "message")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sending_start",
        "status",
    )
    list_filter = (
        "status",
        "message",
    )
    search_fields = ("message", "recipient_list")


@admin.register(MailingTry)
class MailingTryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_time",
        "status",
    )
    list_filter = ("status",)
    search_fields = (
        "response",
        "mailing",
    )
