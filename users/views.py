import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from .forms import UserRegisterForm
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


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.has_perm('users.view_user')


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'user_block_confirm.html'
    fields = ['is_active',]
    success_url = reverse_lazy('users:user_list')

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
