import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER

from .forms import UserForm, UserRegisterForm
from .models import User


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("mailings:home")

    @staticmethod
    def send_email_confirm(user_email, url):
        subject = "Успешная регистрация!"
        message = f"Для подтверждения email перейдите по ссылке: {url}"
        from_email = EMAIL_HOST_USER
        recipient_list = [
            user_email,
        ]
        send_mail(subject, message, from_email, recipient_list)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}/"
        self.send_email_confirm(user.email, url)
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'

    def has_permission(self):
        user = self.request.user
        return user.has_perm('users.view_user')


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_profile.html'


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_profile_form.html'
    success_url = reverse_lazy('mailings:home')


class UserBlockView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_active:
            user.is_active = False
            messages.warning(request, f"Пользователь {user.email} заблокирован.")
        else:
            user.is_active = True
            messages.warning(request, f"Пользователь {user.email} разблокирован.")
        user.save()

        return redirect("users:user_list")

    def has_permission(self):
        user = self.request.user
        return user.has_perm('users.can_block_user')


class UserPasswordResetView(PasswordResetView):
    template_name = 'custom_registration/password_reset_form.html'
    email_template_name = 'custom_registration/password_reset_email.html'
    success_url = reverse_lazy("users:password_reset_done")


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "custom_registration/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")
