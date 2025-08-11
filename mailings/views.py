import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from config.settings import EMAIL_HOST_USER
from .forms import RecipientForm, MessageForm, MailingForm
from .models import Recipient, Message, Mailing, MailingTry


class HomeTemplateView(TemplateView):
    template_name = "mailings/home.html"


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def has_permission(self):
        user = self.request.user
        recipient = self.get_object()
        return user == recipient.owner


class RecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailings/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def has_permission(self):
        user = self.request.user
        recipient = self.get_object()
        return user == recipient.owner


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def has_permission(self):
        user = self.request.user
        message = self.get_object()
        return user == message.owner


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def has_permission(self):
        user = self.request.user
        message = self.get_object()
        return user == message.owner


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def has_permission(self):
        user = self.request.user
        mailing = self.get_object()
        return user == mailing.owner


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def has_permission(self):
        user = self.request.user
        mailing = self.get_object()
        return user == mailing.owner


class MailingTryListView(LoginRequiredMixin, ListView):
    model = MailingTry


class MailingTryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingTry

    def has_permission(self):
        user = self.request.user
        mailing_try = self.get_object()
        return user == mailing_try.mailing.owner or user.has_perm('users.view_user')


class MailingTryView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
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
                mailing.status = 'Завершена'
                mailing.save()


        return redirect("mailings:mailing_list")
