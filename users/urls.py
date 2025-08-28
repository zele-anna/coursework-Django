from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path

from users.apps import UsersConfig
from users.services import email_verification
from users.views import (RegisterView, UserBlockView, UserListView, UserPasswordResetConfirmView,
                         UserPasswordResetView, UserProfileDetailView, UserProfileUpdateView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailings:home"), name="logout"),
    path('reset_password/', UserPasswordResetView.as_view(), name='password_reset'),
    path(
        'reset_password_sent/',
        PasswordResetDoneView.as_view(template_name='custom_registration/password_reset_done.html'),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(
        'password_reset_complete/',
        PasswordResetCompleteView.as_view(template_name='custom_registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path("email_confirm/<str:token>/", email_verification, name="email_confirm"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user/<int:pk>/block/", UserBlockView.as_view(), name="user_block"),
    path("user_profile/<int:pk>/", UserProfileDetailView.as_view(), name="user_profile"),
    path("user_profile/<int:pk>/update/", UserProfileUpdateView.as_view(), name="user_profile_update"),
]
