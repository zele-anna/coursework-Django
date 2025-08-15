from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from users.models import User


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy("users:login"))
