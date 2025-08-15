from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, MailingTry, Message, Recipient
from .services import run_mailing


class HomeTemplateView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'mailings_count': Mailing.objects.filter(owner=self.request.user).count(),
            'mailings_in_process': Mailing.objects.filter(owner=self.request.user, status='Запущена').count(),
            'recipient_count': Recipient.objects.filter(owner=self.request.user).count(),
        })
        return context_data


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient


@method_decorator(cache_page(60 * 5), name='dispatch')
class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        '''Метод для присвоения пользователя в качестве владельца объекта получателя.'''
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


@method_decorator(cache_page(60 * 5), name='dispatch')
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        '''Метод для присвоения пользователя в качестве владельца сообщения.'''
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


@method_decorator(cache_page(60 * 5), name='dispatch')
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_kwargs(self):
        '''Метод для фильтрации списка получателей и сообщений в форме создания рассылки.'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        '''Метод для присвоения пользователя в качестве владельца рассылки.'''
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

    def get_form_kwargs(self):
        '''Метод для фильтрации списка получателей и сообщений в форме обновления рассылки.'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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


@method_decorator(cache_page(60 * 30), name='dispatch')
class MailingTryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingTry

    def has_permission(self):
        user = self.request.user
        mailing_try = self.get_object()
        return user == mailing_try.mailing.owner or user.has_perm('users.view_user')


class MailingTryView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if mailing.status == 'Завершена':
            messages.warning(request, "Рассылка уже завершена и не может быть запущена.")
            return redirect("mailings:mailing_list")

        run_mailing(mailing)

        messages.warning(request, f"Рассылка ID {mailing.pk} запущена.")
        return redirect("mailings:mailing_list")


class MailingStopView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.status = "Завершена"
        mailing.save()

        return redirect("mailings:mailing_list")
