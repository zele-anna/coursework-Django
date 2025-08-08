from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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
